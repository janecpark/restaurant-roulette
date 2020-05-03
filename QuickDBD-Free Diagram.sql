-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/UKShBK
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "User" (
    "UserID" int   NOT NULL,
    "FirstName" string   NOT NULL,
    "Preferences" string   NOT NULL,
    "Email" string   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "UserID"
     )
);

CREATE TABLE "Restaurant" (
    "YelpID" int   NOT NULL,
    "Name" string   NOT NULL,
    "CuisineID" string   NOT NULL,
    "Rating" int   NOT NULL,
    "PriceRange" int   NOT NULL,
    CONSTRAINT "pk_Restaurant" PRIMARY KEY (
        "YelpID"
     )
);

CREATE TABLE "Cuisine" (
    "CuisineID" str   NOT NULL,
    CONSTRAINT "pk_Cuisine" PRIMARY KEY (
        "CuisineID"
     )
);

CREATE TABLE "Preferences" (
    "UserID" int   NOT NULL,
    "CuisineID" string   NOT NULL,
    "Rating" int   NOT NULL,
    "PriceRange" float   NOT NULL,
    "Location" string   NOT NULL
);

CREATE TABLE "Favorite" (
    "FavoriteID" int   NOT NULL,
    "RestaurantID" int   NOT NULL,
    "UserID" int   NOT NULL,
    CONSTRAINT "pk_Favorite" PRIMARY KEY (
        "FavoriteID"
     )
);

ALTER TABLE "Restaurant" ADD CONSTRAINT "fk_Restaurant_CuisineID" FOREIGN KEY("CuisineID")
REFERENCES "Cuisine" ("CuisineID");

ALTER TABLE "Preferences" ADD CONSTRAINT "fk_Preferences_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");

ALTER TABLE "Preferences" ADD CONSTRAINT "fk_Preferences_CuisineID" FOREIGN KEY("CuisineID")
REFERENCES "Cuisine" ("CuisineID");

ALTER TABLE "Favorite" ADD CONSTRAINT "fk_Favorite_RestaurantID" FOREIGN KEY("RestaurantID")
REFERENCES "Restaurant" ("YelpID");

ALTER TABLE "Favorite" ADD CONSTRAINT "fk_Favorite_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");

