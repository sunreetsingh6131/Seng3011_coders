To read the schema:
* Any text within angled brackets should be replaced by some other json, as follows:
* If the text within the angled brackets mentions a json type such as 'string', or 'number', it should be replaced with the appropriate type. For example, if in the schema, you encounter text such as '\<string>' or '\<number\>', in your json file, these should be replaced by a valid JSON string or valid JSON number respectively.
* If the text within the angled bracket mentions some json type with two colons and then a name, it refers to a subsection of this document that will describe the json that should replace the angled bracket. For example, if you encounter '\<string::date\>' within the schema, look for a section of this document called '\<string::date\>'. That section will describe what you should insert in those places.
* As usual, `{}` refers to a json object and `[]` refers to a json array.
* See https://www.json.org/ for more info on the json format.

# [object::article](article.json)
An object containing information about an article.

# [object::report](report.json)
An object containing information about 1 or more events (death, reports, etc) of a disease and/or syndromes.

The array of diseases represent a disjunction. That is, if three diseases are listed that means this object represents one of those, but it is uncertain which.

The array of syndromes is a conjunction. That is, if three syndromes are listed, all three are associated with this object.

# [object::event-report](event-report.json)
An object listing the details of an event, including the type (presence, death, etc), the date the event occurred and the location in which it occurred. The number-affected field contains the number affected by this event. For example, if this event report regards 10 infected, then the type is "infected" and the number-affected is 10.

# string::date

A `date` should be either a `date-exact` or a `date-range`.

# string::date-exact

`yyyy-mm-ddThh:mm:ss` format. Year is mandatory, every other segment is optional. Use 'x' character if missing. String must match the following regular expression: (you can use https://regex101.com/ to test this)

`^(\d{4})-(\d\d|xx)-(\d\d|xx)T(\d\d|xx):(\d\d|xx):(\d\d|xx)$`

Of course, invalid dates (such as `1996-99-99T30:90:90`) are not allowed.

# string::date-range
Let d1 and d2 both be of format `date-exact` (see section above). Then, `date-range` must follow format:

`d1 to d2`

And furthermore d1 must be a date before d2.

See the full specification for examples.

# string::event-type

One of:
* `"presence"`
* `"death"`
* `"infected"`
* `"hospitalised"`
* `"recovered"`

# string::disease

An identifier corresponding to the name of a disease listed in the supplementary file [disease_list.json](../datasets/disease_list.json). You should assume [disease_list.json](../datasets/disease_list.json) is a file that will be updated when new diseases emerge and cater API output to consider them dynamically.

# string::syndrome

An identifier corresponding to the name of a syndrome listed in the supplementary file [syndrome_list.json](../datasets/syndrome_list.json). You should assume [syndrome_list.json](../datasets/syndrome_list.json) is a file that will be updated when new syndromes emerge and cater API output to consider them dynamically.

# object::location

The complications involved in storing locations can be a 3 month project in and of itself. So two versions will be allowed, a basic and an advanced version.

For the [basic verison](location-basic.json), country is the country name and location contains any other details about the location (e.g. province, city, etc.)

For the [advanced version](location-advanced.json), the geonames-id field refers to a geonames ID from the geonames database (http://www.geonames.org/).