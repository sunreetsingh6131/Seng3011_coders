import * as Api from "./ApiTypes";

const myEvent: Api.IEventReport = {
    type: Api.EventType.DEATH,
    date: {date: "1996", type: "exact"},
    "number-affected": 2,
    location: [{"geonames-id": 1},{location: "paris", country: "Australia"}]
};

const myReport: Api.IReport = {
    disease: [{name: "disease"}],
    syndrome: [{name: "syndrome"}],
    reported_events: [myEvent],
    comment: "Nah"
};

const example: Api.IArticle = {
    url: "",
    date_of_publication: { date: "1996", type: "exact" },
    headline: "aa",
    main_text: "Wooo",
    reports: [myReport],
};

switch(example.date_of_publication.type) {
    case "exact":
        console.log(example.date_of_publication.date);
        break;
    case "range":
        console.log(example.date_of_publication.to);
        console.log(example.date_of_publication.from);
        break;
}