import 'package:app/bar%20graph/bar_data.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class MyBarGraph extends StatelessWidget {
  final List weeklySummary;
  const MyBarGraph({
    super.key,
    required this.weeklySummary,
  });

  @override
  Widget build(BuildContext context) {
    //initialize bar data
    BarData myBarData = BarData(
      monRevenue: weeklySummary[0],
      tueRevenue: weeklySummary[1],
      wedRevenue: weeklySummary[2],
      thuRevenue: weeklySummary[3],
      friRevenue: weeklySummary[4],
    );

    myBarData.intializeBarData();

    return BarChart(
      BarChartData(
        //minY: 0,
        //maxY: 100,
        barGroups: myBarData.barData
            .map(
              (data) => BarChartGroupData(
                x: data.x,
                barRods: [
                  BarChartRodData(toY: data.y),
                ],
              ),
            )
            .toList(),
      ),
    );
  }
}
