import 'package:flutter/material.dart';

class Config {
  static String ipAdrress = "192.168.2.19";
  //static String ipAdrress = "10.51.252.248";
  static String baseUrl = "http://$ipAdrress:3000/api/v1";
  static String cafeName = "Tore et fraction";
  static Color specialBlue = const Color.fromARGB(255, 138, 199, 249);
  static Color specialBlueLighter = Colors.lightBlue[100]!;
}
