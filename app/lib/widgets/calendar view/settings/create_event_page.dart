import 'package:app/widgets/calendar%20view/horaire%20widgets/add_event_form.dart';
import 'package:app/widgets/calendar%20view/main%20widgets/app_colors.dart';
import 'package:calendar_view/calendar_view.dart';
import 'package:flutter/material.dart';

class CreateEventPage extends StatelessWidget {
  const CreateEventPage({super.key, this.event});

  final CalendarEventData? event;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Theme.of(context).scaffoldBackgroundColor,
        centerTitle: false,
        leading: IconButton(
          onPressed: () {
            Navigator.pop(context);
          },
          icon: Icon(
            Icons.arrow_back,
            color: AppColors.black,
          ),
        ),
        title: Text(
          event == null ? "Create New Event" : "Update Event",
          style: TextStyle(
            color: AppColors.black,
            fontSize: 20.0,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: SingleChildScrollView(
        physics: ClampingScrollPhysics(),
        child: Padding(
          padding: EdgeInsets.all(20.0),
          child: AddOrEditEventForm(
            onEventAdd: (newEvent) {
              if (this.event != null) {
                CalendarControllerProvider.of(context)
                    .controller
                    .update(this.event!, newEvent);
              } else {
                CalendarControllerProvider.of(context).controller.add(newEvent);
              }

              Navigator.of(context).pop(true);
            },
            event: event,
          ),
        ),
      ),
    );
  }
}
