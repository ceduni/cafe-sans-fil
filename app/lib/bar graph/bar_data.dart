import 'package:app/bar%20graph/individual_bar.dart';

class BarData {
  final double monRevenue;
  final double tueRevenue;
  final double wedRevenue;
  final double thuRevenue;
  final double friRevenue;

  BarData(
      {required this.monRevenue,
      required this.tueRevenue,
      required this.wedRevenue,
      required this.thuRevenue,
      required this.friRevenue});

  List<IndividualBar> barData = [];

  void intializeBarData() {
    barData = [
      IndividualBar(x: 1, y: monRevenue),
      IndividualBar(x: 2, y: tueRevenue),
      IndividualBar(x: 3, y: wedRevenue),
      IndividualBar(x: 4, y: thuRevenue),
      IndividualBar(x: 5, y: friRevenue),
    ];
  }
}
