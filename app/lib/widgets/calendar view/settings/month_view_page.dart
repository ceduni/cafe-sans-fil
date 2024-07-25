import 'package:app/widgets/calendar%20view/horaire%20widgets/month_view_widget.dart';
import 'package:app/widgets/calendar%20view/main%20widgets/extension.dart';
import 'package:app/widgets/calendar%20view/settings/create_event_page.dart';
import 'package:flutter/material.dart';

class MonthViewPageDemo extends StatefulWidget {
  const MonthViewPageDemo({
    super.key,
  });

  @override
  _MonthViewPageDemoState createState() => _MonthViewPageDemoState();
}

class _MonthViewPageDemoState extends State<MonthViewPageDemo> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        elevation: 8,
        onPressed: () => context.pushRoute(CreateEventPage()),
      ),
      body: MonthViewWidget(),
    );
  }
}
