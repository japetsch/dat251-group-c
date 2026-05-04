import { error } from "@sveltejs/kit";
import { createLoadClient } from "$lib/api/client";
import type { PageLoad } from "./$types";
import type { AdminCalendarAppointment } from "$lib/types/admin";

type DashboardAppointment = AdminCalendarAppointment;

export const load: PageLoad = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);

  const bloodbanksRes = await client.GET("/admin/bloodbank");

  if (bloodbanksRes.error || !bloodbanksRes.data) {
    throw error(500, "Failed to load blood banks");
  }

  const accessibleBloodbanks = bloodbanksRes.data.filter(
    (bloodbank) => bloodbank.user_has_admin_access,
  );

  if (accessibleBloodbanks.length === 0) {
    return {
      bloodbank: null,
      appointmentSlots: [],
      appointments: [],
      stats: {
        todayCount: 0,
        pendingCount: 0,
        completedCount: 0,
      },
      nextAppointment: null,
    };
  }

  const activeBloodbank = accessibleBloodbanks[0];

  const appointmentsRes = await client.GET(
    "/admin/bloodbank/{bloodbank_id}/appointment",
    {
      params: {
        path: {
          bloodbank_id: activeBloodbank.bloodbank_id,
        },
      },
    },
  );

  if (appointmentsRes.error || !appointmentsRes.data) {
    throw error(500, "Failed to load appointments");
  }

  const appointmentSlots = appointmentsRes.data;

  const appointments: DashboardAppointment[] = appointmentSlots.flatMap(
    (slot) =>
      slot.appointments.map((appointment) => ({
        ...appointment,
        time: slot.bookingslot_time,
        bloodbank_name: "",
      })),
  );

  const activeAppointments = appointments.filter(
    (appointment) => !appointment.appointment_cancelled,
  );

  activeAppointments.sort(
    (a, b) => new Date(a.time).getTime() - new Date(b.time).getTime(),
  );

  const nextAppointment = activeAppointments[0] ?? null;

  return {
    bloodbank: activeBloodbank,
    appointmentSlots,
    appointments: activeAppointments,
    stats: {
      todayCount: activeAppointments.length,
      pendingCount: activeAppointments.filter(
        (appointment) => appointment.donations.length === 0,
      ).length,
      completedCount: activeAppointments.filter(
        (appointment) => appointment.donations.length > 0,
      ).length,
    },
    nextAppointment,
  };
};
