import 'package:app/side_bar.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class Article extends StatelessWidget {
  const Article({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: const Text('Article'),
      ),
      body: PieChart(PieChartData(
        sections: [
          PieChartSectionData(
            value: 450,
            color: Colors.amber,
            title: 'one',
            showTitle: true,
            radius: 120,
          ),
          PieChartSectionData(
            value: 700,
            color: Colors.redAccent,
            title: 'two',
            showTitle: true,
            radius: 120,
          ),
          PieChartSectionData(
            value: 123,
            color: Colors.teal,
            title: 'three',
            showTitle: true,
            radius: 120,
          ),
        ],
      )),
    );
  }
}
