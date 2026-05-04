import type { components } from "$lib/api/schema";

export type Appointment = components["schemas"]["AvailableBookingSlot"];

export type AppointmentWithFormattedTime = Appointment & {
  formattedTime: string;
};

export type DonorCalendarAppointment = components["schemas"]["AppointmentType"];

export type PlannerColumn = {
  dayName: string;
  dateLabel: string;
  appointments: AppointmentWithFormattedTime[];
};
