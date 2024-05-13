export const timezone = {

  getSupportedTimezones: () => {
    return Intl.supportedValuesOf('timeZone');
  },

  // https://stackoverflow.com/questions/10087819/convert-date-to-another-timezone-in-javascript
  changeTimezone: (date: Date, timezone: string) => {
    return new Date(
      date.toLocaleString('en-US', {timeZone: timezone})
    );
  }
}


