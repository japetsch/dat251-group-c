import { createLoadClient } from "$lib/api/client";
import type { AdminCalendarAppointment } from "$lib/types/admin";
import type { PageLoad } from "./$types";

type AdminApptPreloaded = {
  appointments: AdminCalendarAppointment[];
  error: string | null;
};

export const load: PageLoad<AdminApptPreloaded> = async ({ fetch, url }) => {
  const client = createLoadClient(fetch, url);
  const bloodbanks = await client.GET("/admin/bloodbank");

  if (!bloodbanks.response.ok || !bloodbanks.data) {
    return {
      appointments: [],
      error: "Failed to load blood banks",
    };
  }

  const selectedBloodbank = bloodbanks.data.find(
    (x) => x.user_has_admin_access,
  );
  if (!selectedBloodbank) {
    return {
      appointments: [],
      error: "No blood bank found for this admin",
    };
  }

  const r = await client.GET("/admin/bloodbank/{bloodbank_id}/appointment", {
    params: {
      path: {
        bloodbank_id: selectedBloodbank.bloodbank_id,
      },
      query: {
        after: "2026-01-01T00:00:00Z",
        show_cancelled: true,
      },
    },
  });

  if (!r.response.ok || !r.data) {
    return {
      appointments: [],
      error: "Failed to load appointments",
    };
  }

  const appointments: AdminCalendarAppointment[] = r.data.flatMap((slot) =>
    slot.appointments.map((appointment) => ({
      ...appointment,
      time: slot.bookingslot_time,
      bloodbank_name: selectedBloodbank.name,
    })),
  );

  return {
    appointments: appointments,
    error: null,
  };
};
