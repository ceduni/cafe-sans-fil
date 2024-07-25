import 'dart:ui';

import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:app/widgets/calendar%20view/settings/home_page.dart';
import 'package:calendar_view/calendar_view.dart';

import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';

DateTime get _now => DateTime.now();

class Horaire extends StatelessWidget {
  const Horaire({super.key});

  @override
  Widget build(BuildContext context) {
    List<CalendarEventData> _events = [
      CalendarEventData(
        date: _now,
        title: "Project meeting",
        description: "Today is project meeting.",
        startTime: DateTime(_now.year, _now.month, _now.day, 18, 30),
        endTime: DateTime(_now.year, _now.month, _now.day, 22),
      ),
      CalendarEventData(
        date: _now.add(Duration(days: 1)),
        startTime: DateTime(_now.year, _now.month, _now.day, 18),
        endTime: DateTime(_now.year, _now.month, _now.day, 19),
        title: "Wedding anniversary",
        description: "Attend uncle's wedding anniversary.",
      ),
      CalendarEventData(
        date: _now,
        startTime: DateTime(_now.year, _now.month, _now.day, 14),
        endTime: DateTime(_now.year, _now.month, _now.day, 17),
        title: "Football Tournament",
        description: "Go to football tournament.",
      ),
      CalendarEventData(
        date: _now.add(Duration(days: 3)),
        startTime: DateTime(
            _now.add(Duration(days: 3)).year,
            _now.add(Duration(days: 3)).month,
            _now.add(Duration(days: 3)).day,
            10),
        endTime: DateTime(
            _now.add(Duration(days: 3)).year,
            _now.add(Duration(days: 3)).month,
            _now.add(Duration(days: 3)).day,
            14),
        title: "Sprint Meeting.",
        description: "Last day of project submission for last year.",
      ),
      CalendarEventData(
        date: _now.subtract(Duration(days: 2)),
        startTime: DateTime(
            _now.subtract(Duration(days: 2)).year,
            _now.subtract(Duration(days: 2)).month,
            _now.subtract(Duration(days: 2)).day,
            14),
        endTime: DateTime(
            _now.subtract(Duration(days: 2)).year,
            _now.subtract(Duration(days: 2)).month,
            _now.subtract(Duration(days: 2)).day,
            16),
        title: "Team Meeting",
        description: "Team Meeting",
      ),
      CalendarEventData(
        date: _now.subtract(Duration(days: 2)),
        startTime: DateTime(
            _now.subtract(Duration(days: 2)).year,
            _now.subtract(Duration(days: 2)).month,
            _now.subtract(Duration(days: 2)).day,
            10),
        endTime: DateTime(
            _now.subtract(Duration(days: 2)).year,
            _now.subtract(Duration(days: 2)).month,
            _now.subtract(Duration(days: 2)).day,
            12),
        title: "Chemistry Viva",
        description: "Today is Joe's birthday.",
      ),
    ];
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_hourlyTitle),
        surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
      ),
      body: CalendarControllerProvider(
        controller: EventController()..addAll(_events),
        child: MaterialApp(
          title: 'Flutter Calendar Page Demo',
          debugShowCheckedModeBanner: false,
          theme: ThemeData.light(),
          scrollBehavior: ScrollBehavior().copyWith(
            dragDevices: {
              PointerDeviceKind.trackpad,
              PointerDeviceKind.mouse,
              PointerDeviceKind.touch,
            },
          ),
          home: const HomePage(),
        ),
      ),
    );
  }
}
