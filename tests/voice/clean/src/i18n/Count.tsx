export const Count = ({ a, b }: { a: number; b: number }) => (
  <Text>
    {a > 0 && b < 9 ? 'Saved' : 'None'} for the developers (optional)
  </Text>
);
const sorted = items.filter(x => x.size > 3 && x.size < 8);
// Code that only looks like JSX text: a comparison, not copy.
const beats = (them: number, us: number, best: number) => them>us && us<best;
// Generics look like tags: these are types, not copy.
export function pair(a: Array<number>, us: Array<number>): Map<string, number> { return new Map(); }
export const Either = ({ busy }: { busy: boolean }) =>
  busy ? (
    <Bar />
  ) : (
    // Not loaded yet: we cannot know how many there are.
    <>
      <Text>Load</Text>
    </>
  );
