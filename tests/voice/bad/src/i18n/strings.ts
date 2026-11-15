const cs: Record<string, string> = {
  'sms': 'Jednorázový kód jsme vám poslali v SMS.',
  'remind': 'Upozorníme vás den předem.',
  'backup': 'Zálohu neotevře nikdo, ani my.',
};
const en: Record<string, string> = {
  'telemetry': "When it's on, we'll send a description.",
  'backup': 'Nobody opens the backup, including us.',
};
const faq = { privacy: { cs: 'Data neprodáváme.', en: 'Our servers keep nothing.' } };
// practices-allow voice: quote
const quoted = 'We said so';
const banner = { en: 'WE NEVER SELL IT' };
const pick = (keep: boolean) => (keep ? 'We keep it for you.' : 'Kept.');
