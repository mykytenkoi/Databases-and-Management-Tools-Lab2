#!/usr/bin/env python
import itertools
import pprint

from .dynamicsearch import *

__all__ = ["UserDynamicSearch", "CallDynamicSearch"]


class UserDynamicSearch(DynamicSearchBase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name: str = "User"
		self.search: dict[self.SearchCriterias[CompareConstant]] = {
			"Name": SearchCriterias(f'"a"."Name"', f"Name", "varchar"),
			"Surname": SearchCriterias(f'"a"."Surname"', f"Surname", "varchar"),
			"Patronymic": SearchCriterias(f'"a"."Patronymic"', "Patronymic", "varchar"),

			"Call_time_left": SearchCriterias(f'"a"."Call_time_left"', f"Call_time_left", "bigint"),
			"Trafic_left": SearchCriterias(f'"a"."Trafic_left"', f"Trafic_left", "bigint"),
			"SMS_left": SearchCriterias(f'"a"."SMS_left"', f"SMS_left", "bigint"),

			"TariffName": SearchCriterias(f'"b"."Name"', f"TariffName", "varchar"),
			"TariffPrice": SearchCriterias(f'"b"."Price"', f"TariffPrice", "money"),
			"TariffCall_time": SearchCriterias(f'"b"."Call_time"', f"TariffCall_time", "bigint"),
			"TariffTrafic": SearchCriterias(f'"b"."Trafic"', f"TariffTrafic", "bigint"),
			"TariffSMS": SearchCriterias(f'"b"."SMS"', f"TariffSMS", "bigint"),
		}

	@property
	def sql(self):
		where = self.where
		sql = f"""
			SELECT
				"a"."Name" as "Name",
				"a"."Surname" as "Surname",
				"a"."Patronymic" as "Patronymic",

				"a"."Call_time_left" as "Call_time_left",
				"a"."Trafic_left" as "Trafic_left",
				"a"."SMS_left" as "SMS_left",

				"b"."Name" as "TariffName",
				"b"."Price" as "TariffPrice",
				"b"."Call_time" as "TariffCall_time",
				"b"."Trafic" as "TariffTrafic",
				"b"."SMS" as "TariffSMS"

			FROM
				"{self.schema}"."User" as "a"
				INNER JOIN "{self.schema}"."Tariff" as "b"
					ON "a"."TariffID" = "b"."id"
			{f'''WHERE
				{where};''' if where else f";"}
		"""

		return sql


class CallDynamicSearch(DynamicSearchBase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name: str = "Call"
		self.search: dict[self.SearchCriterias[CompareConstant]] = {
			"Call_time": SearchCriterias(f'"a"."Call_time"', "Call_time", "timestamp"),
			"Duration": SearchCriterias(f'"a"."Duration"', "Duration", "bigint"),

			"FromName": SearchCriterias(f'"b"."Name"', f"FromName", "varchar"),
			"FromSurname": SearchCriterias(f'"b"."Surname"', f"FromSurname", "varchar"),
			"FromPatronymic": SearchCriterias(f'"b"."Patronymic"', "FromPatronymic", "varchar"),

			"ToName": SearchCriterias(f'"c"."Name"', f"ToName", "varchar"),
			"ToSurname": SearchCriterias(f'"c"."Surname"', f"ToSurname", "varchar"),
			"ToPatronymic": SearchCriterias(f'"c"."Patronymic"', "ToPatronymic", "varchar"),
		}

	@property
	def sql(self):
		where = self.where
		sql = f"""
			SELECT
				"a"."Call_time" as "Call_time",
				"a"."Duration" as "Duration",

				"b"."Name" as "FromName",
				"b"."Surname" as "FromSurname",
				"b"."Patronymic" as "FromPatronymic",

				"c"."Name" as "ToName",
				"c"."Surname" as "ToSurname",
				"c"."Patronymic" as "ToPatronymic"

			FROM
				"{self.schema}"."Call" as "a"
				INNER JOIN "{self.schema}"."User" as "b"
					ON "a"."User_from" = "b"."id"
				INNER JOIN "{self.schema}"."User" as "c"
					ON "a"."User_to" = "c"."id"
			{f'''WHERE
				{where};''' if where else f";"}
		"""

		return sql


def _test():
	pass


if __name__ == "__main__":
	_test()
