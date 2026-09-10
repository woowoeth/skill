---
name: parquet-explorer
description: Profiles and explores .parquet files -- schema, row count, per-column stats (nulls, uniques, min/max/mean), and a sample of rows. Use this whenever the user mentions a .parquet file, asks what's in one, wants to inspect/preview/understand a parquet dataset, or references a path ending in .parquet -- even if they don't explicitly say "parquet" or "profile" (e.g. "what's in this data file", "can you check this export"). Also use it as the first step before any deeper analysis, filtering, or conversion of a parquet file, so the data's shape and quirks are known before working with it further.
---

# Parquet Explorer

Parquet files are columnar and can be huge, so the instinct to `pd.read_parquet(path)` and
then poke around is often the wrong first move -- it can mean pulling gigabytes into memory
just to answer "what columns does this have?" This skill profiles a parquet file cheaply
first, then only reads as much actual data as the question requires.

## Workflow

1. **Run the bundled profiler first**, always, on any parquet file you're asked about:

   ```bash
   python3 scripts/profile_parquet.py <path/to/file.parquet>
   ```

   This reads the file's metadata (schema, row count, row groups) without loading the
   data, then samples up to 10,000 rows (via `--sample-rows`) to compute per-column stats
   and show a preview. It prints a markdown report to stdout.

   For a very wide or many-row file where even the default sample feels slow, lower
   `--sample-rows`; for a small file, there's no harm raising it or dropping it entirely
   for exact stats (schema and row count are always exact regardless of sample size,
   since they come straight from the file's metadata footer).

2. **Share the profile inline in your reply** -- the schema table, row count, column
   stats, and sample rows are usually exactly what someone wants when they hand you a
   parquet file. Don't just say "I profiled the file" -- show the actual schema and stats
   in your response.

3. **If the user wants a saved report** (they mention sharing it, keeping it, or the file
   is large enough that a persistent record is useful), rerun with `--output report.md`
   to also write the markdown to disk, and point them at the file.

4. **If the request goes beyond profiling** -- filtering, aggregating, joining, converting
   to another format, plotting -- use the profile's output to inform how you do it (e.g.
   you now know column names, dtypes, and roughly how many rows you're dealing with), then
   write the specific pandas/pyarrow/duckdb code for that task. Don't force everything
   through the profiler script; it's a reconnaissance step, not a general-purpose query tool.

   - For row counts in the tens of millions or more, or when the task is really "run SQL
     against this file," reach for DuckDB (`duckdb.sql("SELECT ... FROM 'file.parquet'")`)
     instead of loading the whole thing into pandas -- it queries parquet directly off disk.
   - For everything else, plain pandas/pyarrow is simpler and is what the profiler itself uses.

## Reading the output

The profile has four sections:

- **Header stats**: row count, column count, row group count, file size, and the writer
  (e.g. `parquet-cpp-arrow`, `pyspark`) -- useful for spotting how the file was produced.
- **Schema**: every column's name, Arrow type, and nullability, read straight from the
  file's footer -- exact even on files too large to fully load.
- **Column stats**: nulls, unique count, and (for numeric/datetime columns) min/max/mean --
  computed from the sample, so treat these as representative rather than exact on very
  large files. The header note says how many rows the stats are based on.
- **Sample rows**: a literal preview of the first rows, for a gut check on what the data
  actually looks like beyond types and summary stats.

## Notes

- The script depends only on `pandas` and `pyarrow` (no `tabulate` or other extras).
- If profiling fails (corrupt file, wrong format, permissions), the script exits with a
  clear error on stderr rather than a raw traceback -- relay that message to the user
  rather than guessing at the cause.
