import 'package:flutter/material.dart';

class AddBenevolInput extends StatefulWidget {
  const AddBenevolInput({super.key});

  @override
  State<AddBenevolInput> createState() => _AddBenevolInputState();
}

class _AddBenevolInputState extends State<AddBenevolInput> {
  double? screenWidth = 390;
  double? screenHeight = 844;
  String selectedOption = 'Option 1';
  final List<String> options = ['Option 1', 'Option 2'];
  @override
  Widget build(BuildContext context) {
    return Builder(builder: (BuildContext context) {
      screenWidth = MediaQuery.of(context).size.width;
      screenHeight = MediaQuery.of(context).size.height;
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: screenHeight != null
                ? EdgeInsets.only(left: screenHeight! * 0.025)
                : EdgeInsets.zero,
            child: const Text(
              "Matricule du benevole",
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.left,
            ),
          ),
          Container(
            padding: const EdgeInsets.all(0.0),
            decoration: BoxDecoration(
              border: Border.all(color: Colors.blueAccent),
              borderRadius: BorderRadius.circular(8),
            ),
            width: screenWidth != null ? screenWidth! * 0.95 : 400.0,
            margin: const EdgeInsets.all(10.0),
            child: const TextField(
              decoration: InputDecoration(
                border: InputBorder.none,
                hintText: "Entrer le matricule du bénévole",
              ),
            ),
          ),
          DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: selectedOption,
              isExpanded: true,
              icon: const Icon(Icons.arrow_downward),
              iconSize: 24,
              elevation: 16,
              style: const TextStyle(color: Colors.black),
              onChanged: (String? newValue) {
                setState(() {
                  selectedOption = newValue!;
                });
              },
              items: options.map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 8.0),
                    child: Text(value),
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      );
    });
  }
}
