import 'package:app/side_bar.dart';
import 'package:flutter/material.dart';

class Evenement extends StatelessWidget {
  const Evenement({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: const Text('Evènement'),
      ),
    );
  }
}
