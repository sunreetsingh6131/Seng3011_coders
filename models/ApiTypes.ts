/*
 * A module containing TypeScript interfaces and types of objects described in the specification.
 *
 * Feel free to change these as you see fit, provided your data model still obeys the specification.
 */

export interface IArticle {
    url: string;
    date_of_publication: ApiDate;
    headline: string;
    main_text: string;
    reports: IReport[];
}

export type ApiDate = IDateExact | IDateRange;

export interface IDateExact {
    type: "exact";
    date: string;
}

export interface IDateRange {
    type: "range";
    from: IDateExact;
    to: IDateExact;
}

export interface IReport {
    disease: IDisease[];
    syndrome: ISyndrome[];
    reported_events: IEventReport[];
    comment: string;
}

export interface IDisease {
    name: string;
}

export interface ISyndrome {
    name: string;
}

export interface IEventReport {
    type: EventType;
    date: ApiDate;
    location: (ILocationBasic | ILocationAdvanced)[];
    "number-affected": number;
}

export enum EventType {
    PRESENCE = "presence",
    DEATH = "death",
    INFECTED = "infected",
    HOSPITALISED = "hospitalised",
    RECOVERED = "recovered",
}

export interface ILocationBasic {
    type: "basic";
    location: string;
    country: string;
}

export interface ILocationAdvanced {
    type: "advanced";
    "geonames-id": number;
}