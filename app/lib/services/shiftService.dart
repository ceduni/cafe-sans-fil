import 'dart:convert';
import 'package:app/config.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:app/modeles/Shift.dart';
import 'package:time_planner/time_planner.dart';

class ShiftService {
  final String baseUrl = "${Config.baseUrl}/shifts";

  ShiftService({dynamic});

  Future<List<Shift>> fetchShifts() async {
    print("in shift service");
    var response = await http.get(Uri.parse(baseUrl));

    if (response.statusCode == 200) {
      var body = json.decode(response.body);

      if (body["Shifts"] != null) {
        print("in json sales tab");
        List<dynamic> shiftsJson = body['Shifts'];

        List<Shift> shifts =
            shiftsJson.map((item) => Shift.fromJson(item)).toList();

        return shifts;
      } else {
        throw Exception('Shift data is not available');
      }
    } else {
      throw Exception('Failed to load sales from $baseUrl');
    }
  }

  List<Shift> getShiftByCafe(List<Shift> shifts, String cafeName) {
    List<Shift> cafeShifts = [];
    for (var shift in shifts) {
      if (shift.cafeName == cafeName) {
        cafeShifts.add(shift);
      }
    }
    return cafeShifts;
  }

  DateTime truncateTime(DateTime date) {
    return DateTime(date.year, date.month, date.day);
  }

  List<DateTime> getFirstAndLastDayOfWeek(DateTime aDay) {
    DateTime firstDayOfWeek =
        truncateTime(aDay.subtract(Duration(days: aDay.weekday - 1)));
    DateTime lastDayOfWeek =
        truncateTime(firstDayOfWeek.add(Duration(days: 6)));
    return [firstDayOfWeek, lastDayOfWeek];
  }

  int getDuration(ShiftDetail shiftDay) {
    int duration = 0;
    List<String> startTime = shiftDay.startTime.split(':');
    List<String> endTime = shiftDay.endTime.split(':');
    duration = int.parse(endTime[0]) - int.parse(startTime[0]);
    return duration;
  }

  List<TimePlannerTask> shiftToTimePlannerTask(
      List<ShiftDetail> shift, String text) {
    List<TimePlannerTask> AllShiftPlan = [];

    for (var shift in shift) {
      int duration = getDuration(shift);
      List<String> startTime = shift.startTime.split(':');

      TimePlannerTask task = TimePlannerTask(
        color: Colors.blueAccent,
        dateTime: TimePlannerDateTime(
          day: shift.date.weekday,
          hour: int.parse(startTime[0]),
          minutes: int.parse(startTime[1]),
        ),
        minutesDuration: duration * 60,
        child: Text(text),
      );
      AllShiftPlan.add(task);
    }
    return AllShiftPlan;
  }

  List<TimePlannerTask> shiftsPlanToDisplay(
      List<Shift> shifts, String cafeName, DateTime dayOfWeek) {
    List<TimePlannerTask> AllShiftPlan = [];
    List<Shift> cafeShifts = getShiftByCafe(shifts, cafeName);
    List<DateTime> firstAndLastDayOfWeek = getFirstAndLastDayOfWeek(dayOfWeek);
    DateTime firstDayOfWeek = firstAndLastDayOfWeek[0];
    DateTime lastDayOfWeek = firstAndLastDayOfWeek[1];

    List<ShiftDetail> shiftToDisplay = [];
    List<String> matriculeForShift = [];

    for (var shifts in cafeShifts) {
      for (ShiftDetail shiftDetail in shifts.shifts) {
        if (shifts.matricule == "20095336") {
          DateTime truncatedShiftDate = truncateTime(shiftDetail.date);
          if (truncatedShiftDate.isAfter(firstDayOfWeek) &&
              truncatedShiftDate.isBefore(lastDayOfWeek)) {
            shiftToDisplay.add(shiftDetail);
            matriculeForShift.add(shifts.matricule);
          }
        }
      }
    }

    for (int i = 0; i < shiftToDisplay.length; i++) {
      AllShiftPlan.addAll(
          shiftToTimePlannerTask(shiftToDisplay, matriculeForShift[i]));
    }

    print(AllShiftPlan);

    return AllShiftPlan;
  }
}
