-- Adminer 4.6.3-dev PostgreSQL dump

\connect "d5m62qnapmclfu";

DROP TABLE IF EXISTS "checkins";
DROP SEQUENCE IF EXISTS checkins_id_seq;
CREATE SEQUENCE checkins_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."checkins" (
    "id" integer DEFAULT nextval('checkins_id_seq') NOT NULL,
    "comnts" character varying(50),
    "userid" integer NOT NULL,
    "loc" integer NOT NULL,
    CONSTRAINT "checkins_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "checkins_userid_loc" UNIQUE ("userid", "loc"),
    CONSTRAINT "checkins_loc_fkey" FOREIGN KEY (loc) REFERENCES zips(id) NOT DEFERRABLE,
    CONSTRAINT "checkins_userid_fkey" FOREIGN KEY (userid) REFERENCES users(id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."users" (
    "username" character varying NOT NULL,
    "password" character varying NOT NULL,
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    CONSTRAINT "users_id" PRIMARY KEY ("id"),
    CONSTRAINT "users_username" UNIQUE ("username")
) WITH (oids = false);


DROP TABLE IF EXISTS "zips";
DROP SEQUENCE IF EXISTS zips_id_seq;
CREATE SEQUENCE zips_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."zips" (
    "id" integer DEFAULT nextval('zips_id_seq') NOT NULL,
    "city" character varying(30) NOT NULL,
    "zip" character varying(5) NOT NULL,
    "lat" double precision NOT NULL,
    "long" double precision NOT NULL,
    "pop" integer NOT NULL,
    "state" character(2) NOT NULL,
    "checkcount" integer DEFAULT '0' NOT NULL,
    CONSTRAINT "zips_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


-- 2018-07-14 21:52:08.359057+00
