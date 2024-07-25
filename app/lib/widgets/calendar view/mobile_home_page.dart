import 'package:app/widgets/calendar%20view/main%20widgets/extension.dart';
import 'package:app/widgets/calendar%20view/settings/day_view_page.dart';
import 'package:app/widgets/calendar%20view/settings/month_view_page.dart';
import 'package:app/widgets/calendar%20view/settings/week_view_page.dart';
import 'package:flutter/material.dart';

class MobileHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Flutter Calendar Page"),
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ElevatedButton(
              onPressed: () => context.pushRoute(MonthViewPageDemo()),
              child: Text("Month View"),
            ),
            SizedBox(
              height: 20,
            ),
            ElevatedButton(
              onPressed: () => context.pushRoute(DayViewPageDemo()),
              child: Text("Day View"),
            ),
            SizedBox(
              height: 20,
            ),
            ElevatedButton(
              onPressed: () => context.pushRoute(WeekViewDemo()),
              child: Text("Week View"),
            ),
          ],
        ),
      ),
    );
  }
}
