# Day 60, Task 9 (ABAP slot) -- ABAP: explain one concept in your own words

(Pick a concept you have NOT already written up -- check the earlier day files in this folder.)

## THE TASK

Pick ONE concept -- suggestions: ABAP Managed Database Procedures (AMDP: `IF_AMDP_MARKER_HDB`, `BY DATABASE PROCEDURE FOR HDB LANGUAGE SQLSCRIPT OPTIONS READ-ONLY USING ...`, why every table must be listed in `USING`, how importing/exporting parameters map to SQLScript table variables, and when "code pushdown" with AMDP is worth it compared to plain ABAP SQL or a CDS view), CDS table functions (`define table function ... returns { ... } implemented by method cl=>m`, the `FOR TABLE FUNCTION` AMDP method, and the client-handling annotation `@ClientHandling.type` / `.algorithm`), or modern ABAP SQL features (common table expressions `WITH +cte AS ( ... )`, `UNION` / `INTERSECT` / `EXCEPT`, window expressions `OVER( PARTITION BY ... )`, host expressions `@( ... )`, and `SELECT ... FROM @itab` to query an internal table) -- and explain it as if teaching a classmate who knows classic ABAP report programs and `SELECT ... ENDSELECT` but has never pushed logic down to the database.

## CONCEPT CHOSEN

Modern ABAP SQL: common table expressions (`WITH +cte AS ( ... )`), set operators (`UNION` / `INTERSECT` / `EXCEPT`), window expressions (`... OVER( PARTITION BY ... ORDER BY ... )`), host expressions `@( ... )`, and `SELECT ... FROM @itab` to run SQL over an internal table. (CDS table functions + AMDP were already covered on day 22, so this is the "pushdown without leaving ABAP SQL" side.)

## MY EXPLANATION (write this BEFORE looking anything up)

The classic style is: `SELECT` raw rows into an internal table (or worse, `SELECT ... ENDSELECT` with nested `SELECT SINGLE`s), then `LOOP` in ABAP to sum, rank, filter and join. That moves a lot of rows over the network from the database to the application server just to throw most of them away. "Code pushdown" means: let the database do the set work and only send back the result. Since 7.40 SP05 / 7.50+ ABAP SQL (the "new" Open SQL with comma-separated lists and `@` host variables) grew most of what you'd write in plain SQL, so a lot of pushdown is possible without AMDP:

- **Common table expressions.** `WITH +name AS ( SELECT ... )` defines a named sub-result (the `+` prefix marks it as a CTE, not a DDIC table). Later CTEs and the main query select `FROM +name` like a table. It breaks one big query into readable steps ("first aggregate per customer, then keep the top ones") and the whole thing is still ONE statement executed by the database. A `WITH` statement ends with the main `SELECT`; if that returns several rows you write it with `INTO TABLE`, or close it with `ENDWITH` when it is a loop.
- **Set operators.** `UNION` (distinct) / `UNION ALL` combine the rows of two selects with compatible columns; `INTERSECT` keeps rows present in both; `EXCEPT` keeps rows from the first that are not in the second (INTERSECT/EXCEPT came after UNION, around 7.53/7.54). Handy for "open items from table A that have no match in B" without a `FOR ALL ENTRIES` + `DELETE` dance.
- **Window expressions.** `ROW_NUMBER( )`, `RANK( )`, `SUM( ... )`, `LAG`/`LEAD` etc. with `OVER( PARTITION BY ... ORDER BY ... )` compute a value per row *relative to its group* without collapsing the rows like `GROUP BY` does -- e.g. "running total per customer", "rank of each order within its customer", "previous order date". Classic ABAP did this with a sorted `LOOP` and `AT NEW` and helper variables.
- **Host expressions.** `@( expression )` lets you put an ABAP expression (method call, `sy-datum - 30`, a constructor expression) right into the `WHERE` or field list; it is evaluated once in ABAP before the statement runs and passed as a parameter. Plain host variables are written `@lv_var`, and `@DATA( ... )` / `@FINAL( ... )` declare the target inline.
- **`FROM @itab`.** An internal table can be the data source of a `SELECT` (it needs an alias: `FROM @lt_orders AS o`). If the statement only touches the itab the ABAP runtime can evaluate it itself; if it is joined with database tables, the itab content is shipped to the database as a temporary table. Useful to apply SQL features (GROUP BY, window functions, joins to DB tables) to data you already have in memory instead of writing a `LOOP` plus `FOR ALL ENTRIES`.

**When to use:** reporting/aggregation over many rows, ranking/top-N per group, "rows in A but not in B", or when the result is much smaller than the input. **When not:** simple single-record reads (a plain `SELECT SINGLE` is fine), logic that needs ABAP-only features (authority checks per row, function modules, complex business rules), very large itabs in `FROM @itab` joined to DB tables (shipping them to the DB costs too), and when a reusable CDS view would serve several consumers -- then put the logic in CDS so it is defined once. If even ABAP SQL can't express it (procedural SQLScript, HANA-specific functions), that's when AMDP comes in. Also note: some newer features are database-dependent; on non-HANA DBs the syntax check may require `##DB_FEATURE_MODE` handling or the feature isn't available, and in ABAP Cloud you can only select from released CDS views anyway.

## A SMALL EXAMPLE

```abap
* Top 3 customers by revenue in the last 90 days, each with its biggest order,
* ranked per country -- one database round trip.
DATA(lv_since) = cl_abap_context_info=>get_system_date( ) - 90.

WITH
  +revenue AS (
    SELECT customer_id, country,
           SUM( net_amount )  AS total,
           MAX( net_amount )  AS biggest_order
      FROM zsales_order
      WHERE order_date >= @lv_since
        AND status     <> @( zcl_order_status=>cancelled )   " host expression
      GROUP BY customer_id, country ),
  +ranked AS (
    SELECT customer_id, country, total, biggest_order,
           RANK( ) OVER( PARTITION BY country ORDER BY total DESCENDING ) AS rnk
      FROM +revenue )
  SELECT customer_id, country, total, biggest_order, rnk
    FROM +ranked
    WHERE rnk <= 3
    ORDER BY country, rnk
    INTO TABLE @DATA(lt_top).

* Customers that bought something but never paid anything: EXCEPT
SELECT customer_id FROM zsales_order
EXCEPT
SELECT customer_id FROM zpayment
  INTO TABLE @DATA(lt_unpaid).

* SQL over an internal table: sum a CSV upload per material without a LOOP
TYPES: BEGIN OF ty_line, matnr TYPE matnr, qty TYPE i, END OF ty_line.
DATA lt_upload TYPE STANDARD TABLE OF ty_line WITH EMPTY KEY.
" ... lt_upload filled from the file ...
SELECT matnr, SUM( qty ) AS qty
  FROM @lt_upload AS u
  GROUP BY matnr
  INTO TABLE @DATA(lt_per_material).
```

## WHAT I GOT WRONG / CHECKED AFTERWARDS

- Checked: in ABAP SQL every CTE name must start with `+` (`+revenue`), both where it is defined and where it is used.
- The ABAP keyword for descending order inside `OVER( ORDER BY ... )` is `DESCENDING` (not `DESC`), same as in a normal ABAP SQL `ORDER BY`.
- `FROM @itab` needs an alias (`AS u`) and the itab may not contain deep/string components in all releases; if it's combined with DB tables the content really is transferred to the database, so it's not "free".
- Release matters: CTEs and `FROM @itab` arrived around 7.51/7.52, window expressions in 7.54 (plus more window functions later), `INTERSECT`/`EXCEPT` in 7.56-ish -- check the system's release before relying on them. On some database platforms certain features need a feature check (`cl_abap_dbfeatures`) or are only available on HANA.
- A host expression `@( ... )` is evaluated in ABAP once before the query, not per row on the database -- it's a parameter, not pushed-down logic.

## ONE-LINE TAKEAWAY

Modern ABAP SQL (CTEs, set operators, window functions, `@( )` host expressions and `FROM @itab`) lets you push grouping, ranking and set logic to the database in one readable statement, so try that before reaching for `LOOP`/`AT NEW` -- or for AMDP.
