export type Appointment = {
	id: number;
	time: string;
	location_id: number;
	locationname: string;
};

export type AppointmentWithFormattedTime = {
	id: number;
	time: string;
	location_id: number;
	locationname: string;
	formattedTime: string;
};

export type PlannerColumn = {
	dayName: string;
	dateLabel: string;
	appointments: AppointmentWithFormattedTime[];
};