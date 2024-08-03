import 'dart:ui';

import 'package:app/provider/shift_provider.dart';
import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:app/widgets/time_planner_widget.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:provider/provider.dart';

class Horaire extends StatefulWidget {
  const Horaire({super.key});

  @override
  State<Horaire> createState() => _HoraireState();
}

class _HoraireState extends State<Horaire> {
  @override
  void initState() {
    super.initState();
    fetch();
  }

  Future<void> fetch() async {
    await context.read<ShiftProvider>().fetchShifts();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_hourlyTitle),
        surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
      ),
      body: Consumer<ShiftProvider>(
        builder: (context, shiftProvider, child) {
          if (shiftProvider.isLoading) {
            return const Center(
              child: CircularProgressIndicator(
                  color: Color.fromARGB(255, 138, 199, 249)),
            );
          } else if (shiftProvider.hasError) {
            return Center(
              child: Text('Error: ${shiftProvider.errorMessage}'),
            );
          } else {
            return TimePlannerWidget();
          }
        },
      ),
    );
  }
}
