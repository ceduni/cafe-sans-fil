import 'package:app/side%20bar/side_bar.dart';
import 'package:flutter/material.dart';

class Article extends StatelessWidget {
  const Article({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: const Text('Article'),
        surfaceTintColor: Colors.blue,
      ),
    );
  }
}
