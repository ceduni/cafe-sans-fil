import 'package:app/widgets/calendar%20view/main%20widgets/constants.dart';
import 'package:flutter/material.dart';

class ResponsiveWidget extends StatelessWidget {
  final double? width;
  final double breakPoint;
  final Widget webWidget;
  final Widget mobileWidget;

  const ResponsiveWidget({
    super.key,
    this.width,
    this.breakPoint = BreakPoints.web,
    required this.webWidget,
    required this.mobileWidget,
  });

  @override
  Widget build(BuildContext context) {
    final width = this.width ?? MediaQuery.of(context).size.width;

    if (width < breakPoint) {
      return mobileWidget;
    } else {
      return webWidget;
    }
  }
}
