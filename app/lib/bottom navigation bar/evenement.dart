import 'package:app/side%20bar/side_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';

class Evenement extends StatelessWidget {
  const Evenement({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_eventTitle),
        surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
      ),
    );
  }
}