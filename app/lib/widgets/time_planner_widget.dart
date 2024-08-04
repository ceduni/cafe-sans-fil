import 'package:app/config.dart';
import 'package:app/provider/shift_provider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:time_planner/time_planner.dart';

class TimePlannerWidget extends StatefulWidget {
  TimePlannerWidget({super.key});

  @override
  State<TimePlannerWidget> createState() => _TimePlannerWidgetState();
}

class _TimePlannerWidgetState extends State<TimePlannerWidget> {
  final List<TimePlannerTask> tasks = [];
  final _formKey = GlobalKey<FormState>();
  final _taskController = TextEditingController();
  int _selectedDay = 0;
  int _startHour = 9;
  int _startMinute = 0;
  int _duration = 60;

  @override
  void initState() {
    for (TimePlannerTask task
        in context.read<ShiftProvider>().shiftsToDisplay) {
      tasks.add(task);
    }
    super.initState();
  }

  void _addTask() {
    if (_formKey.currentState!.validate()) {
      setState(() {
        tasks.add(
          TimePlannerTask(
            color: Config.specialBlue,
            dateTime: TimePlannerDateTime(
              day: _selectedDay,
              hour: _startHour,
              minutes: _startMinute,
            ),
            minutesDuration: _duration,
            child: Text(_taskController.text),
          ),
        );
      });
      _taskController.clear();
      Navigator.of(context).pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: TimePlanner(
        startHour: 6,
        endHour: 22,
        headers: [
          TimePlannerTitle(title: "Lun"),
          TimePlannerTitle(title: "Mar"),
          TimePlannerTitle(title: "Mer"),
          TimePlannerTitle(title: "Jeu"),
          TimePlannerTitle(title: "Ven"),
          TimePlannerTitle(title: "Sam"),
          TimePlannerTitle(title: "Dim"),
        ],
        tasks: tasks,
        style: TimePlannerStyle(
          cellHeight: 70,
          cellWidth: 70,
          dividerColor: Colors.red[900],
          showScrollBar: true,
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          showDialog(
            context: context,
            builder: (context) => AlertDialog(
              title: Text('Add Task'),
              content: Form(
                key: _formKey,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    TextFormField(
                      controller: _taskController,
                      decoration: InputDecoration(labelText: 'Task Name'),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter a task name';
                        }
                        return null;
                      },
                    ),
                    DropdownButtonFormField<int>(
                      decoration: InputDecoration(labelText: 'Day'),
                      value: _selectedDay,
                      items: List.generate(7, (index) {
                        return DropdownMenuItem(
                          value: index,
                          child: Text('Day ${index + 1}'),
                        );
                      }),
                      onChanged: (value) {
                        setState(() {
                          _selectedDay = value!;
                        });
                      },
                    ),
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            decoration:
                                InputDecoration(labelText: 'Start Hour'),
                            keyboardType: TextInputType.number,
                            initialValue: '9',
                            onChanged: (value) {
                              try {
                                _duration = int.parse(value);
                              } on FormatException {
                                _duration = 9;
                              }
                            },
                          ),
                        ),
                        SizedBox(width: 16),
                        Expanded(
                          child: TextFormField(
                            decoration:
                                InputDecoration(labelText: 'Start Minute'),
                            keyboardType: TextInputType.number,
                            initialValue: '0',
                            onChanged: (value) {
                              try {
                                _duration = int.parse(value);
                              } on FormatException {
                                _duration = 20;
                              }
                            },
                          ),
                        ),
                      ],
                    ),
                    TextFormField(
                      decoration:
                          InputDecoration(labelText: 'Duration (minutes)'),
                      keyboardType: TextInputType.number,
                      initialValue: '60',
                      onChanged: (value) {
                        try {
                          _duration = int.parse(value);
                        } on FormatException {
                          _duration = 60;
                        }
                      },
                    ),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  child: Text('Cancel'),
                ),
                ElevatedButton(
                  onPressed: _addTask,
                  child: Text('Add'),
                ),
              ],
            ),
          );
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
