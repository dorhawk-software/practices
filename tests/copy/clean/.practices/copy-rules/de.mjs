// A project's own language: German ships with its rules (check-copy fails without them).
export const rules = [
  { id: "zu-dem", what: "\"zu dem\" is \"zum\"", fix: "Write \"zum\".", find: /(?<!\p{L})zu dem(?!\p{L})/gu, check: (m) => `"${m[0]}" is "zum".` },
];
export const vagueButtons = ["ok", "abbrechen", "ja", "nein"];
