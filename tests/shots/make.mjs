// The test pairs for check-shots, written as PNGs (no packages, no binaries in the repository):
//   same/        fresh and live identical
//   glyph/       live lacks a 7×21 glyph at 60,40 (the lost "í")
//   clock/       only the top 12 rows differ (a status bar's clock)
//   size/        live is one row taller
import { deflateSync } from "node:zlib";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const crcTable = Array.from({ length: 256 }, (_, n) => { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; return c >>> 0; });
const crc = (buf) => { let c = 0xffffffff; for (const b of buf) c = crcTable[(c ^ b) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
const chunk = (kind, data) => { const len = Buffer.alloc(4), sum = Buffer.alloc(4), body = Buffer.concat([Buffer.from(kind, "ascii"), data]); len.writeUInt32BE(data.length); sum.writeUInt32BE(crc(body)); return Buffer.concat([len, body, sum]); };
function png(w, h, paint) {
  const raw = Buffer.alloc(h * (w * 3 + 1));
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const [r, g, b] = paint(x, y), o = y * (w * 3 + 1) + 1 + x * 3; raw[o] = r; raw[o + 1] = g; raw[o + 2] = b; }
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4); ihdr[8] = 8; ihdr[9] = 2;
  return Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk("IHDR", ihdr), chunk("IDAT", deflateSync(raw)), chunk("IEND", Buffer.alloc(0))]);
}
const screen = (x, y) => (y < 12 ? [20, 20, 20] : (x + y) % 9 === 0 ? [200, 180, 90] : [40, 36, 30]);
const out = process.argv[2];
const write = (dir, name, buf) => { mkdirSync(join(out, dir), { recursive: true }); writeFileSync(join(out, dir, name), buf); };
for (const side of ["fresh", "live"]) write(`same/${side}`, "switcher.png", png(120, 90, screen));
write("glyph/fresh", "switcher.png", png(120, 90, (x, y) => (x >= 60 && x < 67 && y >= 40 && y < 61 ? [255, 255, 255] : screen(x, y))));
write("glyph/live", "switcher.png", png(120, 90, screen));
write("clock/fresh", "switcher.png", png(120, 90, screen));
write("clock/live", "switcher.png", png(120, 90, (x, y) => (y < 12 && x > 4 && x < 30 ? [230, 230, 230] : screen(x, y))));
write("size/fresh", "switcher.png", png(120, 90, screen));
write("size/live", "switcher.png", png(120, 91, screen));
