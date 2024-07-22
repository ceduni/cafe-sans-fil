import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class CustomBarChart extends StatefulWidget {
  final Color colorLow = const Color(0xFF3498db);
  final Color colorHigh = const Color(0xFF1abc9c);
  final List<List<double>> allValues;
  final int type;

  const CustomBarChart({
    super.key,
    required this.allValues,
    required this.type,
  });

  @override
  State<StatefulWidget> createState() => AnnualChartState();
}

class AnnualChartState extends State<CustomBarChart> {
  static const List<String> monthNames = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
  ];
  static const List<String> weekDays = [
    'Lun',
    'Mar',
    'Mer',
    'Jeu',
    'Ven',
    'Sam',
    'Dim'
  ];

  Widget bottomTitles(double value, TitleMeta meta) {
    const style = TextStyle(fontSize: 10);
    String text = '';

    switch (widget.type) {
      case 0:
        if (value.toInt() >= 0 && value.toInt() < 12) {
          text = monthNames[value.toInt()];
        }
        break;
      case 1:
        if (value.toInt() >= 0 && value.toInt() < 7) {
          text = weekDays[value.toInt()];
        }
        break;
      default:
        text = '';
        break;
    }

    return SideTitleWidget(
      axisSide: meta.axisSide,
      child: Text(text, style: style),
    );
  }

  Widget leftTitles(double value, TitleMeta meta) {
    if (value == meta.max) {
      return Container();
    }
    const style = TextStyle(
      fontSize: 10,
    );
    return SideTitleWidget(
      axisSide: meta.axisSide,
      child: Text(
        meta.formattedValue,
        style: style,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 1.66,
      child: Padding(
        padding: const EdgeInsets.only(top: 16, right: 16),
        child: LayoutBuilder(
          builder: (context, constraints) {
            final barsSpace = 4.0 * constraints.maxWidth / 400;
            final barsWidth = 8.0 * constraints.maxWidth / 400;
            return BarChart(
              BarChartData(
                alignment: BarChartAlignment.center,
                barTouchData: BarTouchData(
                  enabled: false,
                ),
                titlesData: FlTitlesData(
                  show: true,
                  bottomTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 28,
                      getTitlesWidget: bottomTitles,
                    ),
                  ),
                  leftTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 40,
                      getTitlesWidget: leftTitles,
                    ),
                  ),
                  topTitles: const AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                  rightTitles: const AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                ),
                gridData: FlGridData(
                  show: true,
                  checkToShowHorizontalLine: (value) => value % 10 == 0,
                  getDrawingHorizontalLine: (value) => const FlLine(
                    color: Colors.grey,
                    strokeWidth: 1,
                  ),
                  drawVerticalLine: false,
                ),
                borderData: FlBorderData(
                  show: false,
                ),
                groupsSpace: barsSpace,
                barGroups: getData(widget.allValues, barsWidth, barsSpace),
              ),
            );
          },
        ),
      ),
    );
  }

  List<BarChartGroupData> getData(
      List<List<double>> allValue, double barsWidth, double barsSpace) {
    return allValue.asMap().entries.map((entry) {
      int index = entry.key;
      double valueLow = entry.value.reduce(
          (value, element) => value < element ? value : element); //minimum
      double valueHigh = entry.value.reduce(
          (value, element) => value > element ? value : element); //maximum

      return BarChartGroupData(
        x: index,
        barsSpace: barsSpace,
        barRods: [
          BarChartRodData(
            toY: valueHigh,
            rodStackItems: [
              BarChartRodStackItem(0, valueLow, widget.colorLow),
              BarChartRodStackItem(valueLow, valueHigh, widget.colorHigh),
            ],
            borderRadius: BorderRadius.zero,
            width: barsWidth * 3,
          ),
        ],
      );
    }).toList();
  }
}
