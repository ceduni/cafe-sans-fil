import 'package:app/widgets/calendar%20view/horaire%20widgets/week_view_widget.dart';
import 'package:app/widgets/calendar%20view/main%20widgets/extension.dart';
import 'package:flutter/material.dart';

import 'create_event_page.dart';

class WeekViewDemo extends StatefulWidget {
  const WeekViewDemo({super.key});

  @override
  _WeekViewDemoState createState() => _WeekViewDemoState();
}

class _WeekViewDemoState extends State<WeekViewDemo> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        elevation: 8,
        onPressed: () => context.pushRoute(CreateEventPage()),
      ),
      body: WeekViewWidget(),
    );
  }
}
