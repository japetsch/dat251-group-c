export function getStartOfWeek(dateString: string) {
  const date = new Date(dateString);
  const day = date.getUTCDay();

  let daysFromMonday = day - 1;

  if (day === 0) {
    daysFromMonday = 6;
  }

  date.setUTCDate(date.getUTCDate() - daysFromMonday);
  date.setUTCHours(0, 0, 0, 0);

  return date;
}

export function addDays(date: Date, days: number) {
  const newDate = new Date(date);
  newDate.setUTCDate(newDate.getUTCDate() + days);
  return newDate;
}

export function formatDateKey(date: Date) {
  return date.toISOString().split("T")[0];
}

export function getWeekNumber(date: Date) {
  const tempDate = new Date(
    Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()),
  );

  let day = tempDate.getUTCDay();

  if (day === 0) {
    day = 7;
  }

  tempDate.setUTCDate(tempDate.getUTCDate() + 4 - day);

  const yearStart = new Date(Date.UTC(tempDate.getUTCFullYear(), 0, 1));
  const millisecondsDifference = tempDate.getTime() - yearStart.getTime();
  const daysSinceYearStart = millisecondsDifference / 86400000;
  const weekNumber = Math.ceil((daysSinceYearStart + 1) / 7);

  return weekNumber;
}
