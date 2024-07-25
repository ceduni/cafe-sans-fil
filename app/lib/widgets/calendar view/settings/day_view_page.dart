import 'package:app/widgets/calendar%20view/horaire%20widgets/day_view_widget.dart';

import 'package:app/widgets/calendar%20view/settings/create_event_page.dart';
import 'package:flutter/material.dart';

class DayViewPageDemo extends StatefulWidget {
  const DayViewPageDemo({super.key});

  @override
  _DayViewPageDemoState createState() => _DayViewPageDemoState();
}

class _DayViewPageDemoState extends State<DayViewPageDemo> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        elevation: 8,
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => CreateEventPage(),
            ),
          );
        },
      ),
      body: DayViewWidget(),
    );
  }
}
