import type { components } from "$lib/api/schema";

export type AppointmentTypeAdmin =
  components["schemas"]["AppointmentTypeAdmin"];

export type AdminCalendarAppointment = AppointmentTypeAdmin & {
  time: string;
  bloodbank_name: string;
};

export type NoteType = components["schemas"]["NoteType"];
export type DonationType = components["schemas"]["DonationType"];
