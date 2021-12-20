#!/usr/bin/env python3

from . import DynamicSearch
from .AutoSchema import *


class Telecommunications(Schema):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._dynamicsearch = {a.name: a for a in [DynamicSearch.UserDynamicSearch(self), DynamicSearch.CallDynamicSearch(self)]}
		# self.reoverride()

	def reoverride(self):
		# Table override
		pass

	def reinit(self):
		# sql = f"""
		# 	SELECT table_name FROM information_schema.tables
		# 	WHERE table_schema = '{self}';
		# """
		with self.dbconn.cursor() as dbcursor:
			# dbcursor.execute(sql)
			for a in self.refresh_tables():  # tuple(dbcursor.fetchall()):
				q = f"""DROP TABLE IF EXISTS {a} CASCADE;"""
				# print(q)
				dbcursor.execute(q)

		tables = [
			f"""CREATE SCHEMA IF NOT EXISTS "{self}";""",
			f"""CREATE TABLE "{self}"."Tariff" (
				"id" bigserial PRIMARY KEY,
				"Name" character varying(63) NOT NULL,
				"Price" money NOT NULL, --
				"Call_time" bigint NOT NULL, -- milliseconds
				"Trafic" bigint NOT NULL, -- bytes
				"SMS" bigint NOT NULL
				-- UNIQUE("Name")
			);
			""",
			f"""CREATE TABLE "{self}"."User" (
				"id" bigserial PRIMARY KEY,
				"TariffID" bigint NOT NULL,
				"Name" character varying(63) NOT NULL,
				"Surname" character varying(63) NOT NULL,
				"Patronymic" character varying(63) NOT NULL,
				"Call_time_left" bigint NOT NULL, -- milliseconds
				"Trafic_left" bigint NOT NULL, -- bytes
				"SMS_left" bigint NOT NULL,
				CONSTRAINT "User_TariffID_fkey" FOREIGN KEY ("TariffID")
					REFERENCES "Telecommunications"."Tariff"("id") MATCH SIMPLE
					ON UPDATE NO ACTION
					ON DELETE CASCADE
					NOT VALID
			);
			""",
			f"""CREATE TABLE "{self}"."Call" (
				"id" bigserial PRIMARY KEY,
				"User_from" bigint NOT NULL,
				"User_to" bigint NOT NULL,
				"Call_time" timestamp with time zone NOT NULL,
				"Duration" bigint NOT NULL DEFAULT 0, -- milleseconds
				CONSTRAINT "Call_User_from_fkey" FOREIGN KEY ("User_from")
					REFERENCES "Telecommunications"."User"("id") MATCH SIMPLE
					ON UPDATE NO ACTION
					ON DELETE CASCADE
					NOT VALID,
				CONSTRAINT "Call_User_to_fkey" FOREIGN KEY ("User_to")
					REFERENCES "Telecommunications"."User"("id") MATCH SIMPLE
					ON UPDATE NO ACTION
					ON DELETE CASCADE
					NOT VALID
			);
			""",
		]

		with self.dbconn.cursor() as dbcursor:
			for a in tables:
				dbcursor.execute(a)

		self.dbconn.commit()

		self.refresh_tables()

	def randomFill(self):
		self.tables.Tariff.randomFill(1_000)
		self.tables.User.randomFill(2_000)
		self.tables.Call.randomFill(10_000)


def _test():
	pass


if __name__ == "__main__":
	_test()
