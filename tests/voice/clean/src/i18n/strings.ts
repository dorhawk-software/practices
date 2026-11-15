// The app's copy. Comments may say we and ours: people never read them.
/* Nor here: we, us, our. */
const cs: Record<string, string> = {
  'contact.us': 'Napsat vývojářům',
  'saved': 'Kód vám přišel v SMS.',
  'none': 'Nic odpovídajícího se nenašlo.',
  'topic': 'Téma: {count} zpráv',
  'name': `Ahoj, ${user.name}`,
};
const en: Record<string, string> = {
  'contact.us': 'Write to the developers',
  'welcome': 'Welcome home. Any time, same place.',
  'mine': 'Save my work first',
  'consent': 'I agree to the terms',
  'region': 'Stored in the US region',
  'placeholder': 'Sent by {we}',
  // practices-allow voice: a quote from the statute itself
  'quote': '"We, the citizens", says the act.',
};
const faq = { reach: { cs: 'Aplikace pošle popis chyby.', en: 'The app sends a description.' } };
const words = {
  cs: { tip: 'Slovo „my“ aplikace nepoužívá.', address: 'Mariánské nám. 2, Praha', square: 'nám. Míru 5', browser: 'Otevřete v Chrome; tlačítko Home.' },
  en: { tip: 'The word "we" is never used.', store: 'https://apps.apple.com/us/app/example/id1' },
};
