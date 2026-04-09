import { createLoadClient } from "$lib/api/client";
import type { components } from "$lib/api/schema";
import type { PageLoad } from "./$types";

type AdminCalendarAppointment = {
  appointment_id: number;
  username: string;
  time: string;
  bloodbank_name: string;
  cancelled: boolean;
};

type AdminApptPreloaded = {
  upcoming: AdminCalendarAppointment[];
  previous: AdminCalendarAppointment[];
  error: string | null;
};

export const load: PageLoad<AdminApptPreloaded> = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
  const bloodbanks = await client.GET("/admin/bloodbank");

  if (!bloodbanks.response.ok || !bloodbanks.data) {
    return {
      upcoming: [],
      previous: [],
      error: "Failed to load blood banks",
    };
  }

  const selectedBloodbank = bloodbanks.data.find(
    (x) => x.user_has_admin_access,
  );
  if (!selectedBloodbank) {
    return {
      upcoming: [],
      previous: [],
      error: "No blood bank found for this admin",
    };
  }

  const r = await client.GET("/admin/bloodbank/{bloodbank_id}/appointment", {
    params: {
      path: {
        bloodbank_id: selectedBloodbank.bloodbank_id,
      },
    },
  });

  if (!r.response.ok || !r.data) {
    return {
      upcoming: [],
      previous: [],
      error: "Failed to load appointments",
    };
  }

  const appointments: AdminCalendarAppointment[] = r.data.flatMap((slot) =>
    slot.appointments.map((appointment) => ({
      appointment_id: appointment.appointment_id,
      username: appointment.donor_name,
      time: slot.bookingslot_time,
      bloodbank_name: selectedBloodbank.name,
      cancelled: appointment.appointment_cancelled,
    })),
  );

  const now = new Date();
  return {
    previous: appointments.filter((x) => new Date(x.time) < now),
    upcoming: appointments.filter(
      (x) => !x.cancelled && new Date(x.time) >= now,
    ),
    error: null,
  };
};
