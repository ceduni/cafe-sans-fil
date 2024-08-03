import 'package:app/services/VolunteerService.dart';
import 'package:flutter/material.dart';

import '../../config.dart';

class AddBenevole extends StatefulWidget {
  const AddBenevole({super.key});

  @override
  State<AddBenevole> createState() => _AddBenevoleState();
}

class _AddBenevoleState extends State<AddBenevole> {
  bool _isLoading = false;
  String selectedOption = 'Bénévole';
  final List<String> options = ['Bénévole', 'Admin'];
  final TextEditingController _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ajouter un bénévole'),
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          //title for matricule
          Container(
            padding: EdgeInsets.only(left: screenHeight * 0.025),
            child: const Text(
              "Matricule du benevole",
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.left,
            ),
          ),
          //Textfield for matricule
          Container(
            padding: const EdgeInsets.all(0.0),
            decoration: BoxDecoration(
              border: Border.all(color: Colors.blueAccent),
              borderRadius: BorderRadius.circular(8),
            ),
            width: screenWidth * 0.95,
            margin: const EdgeInsets.all(10.0),
            //Textefield
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(
                border: InputBorder.none,
                hintText: "Entrer le matricule du bénévole",
                hintStyle: TextStyle(color: Colors.grey),
              ),
            ),
          ),
          // title for role
          Container(
            padding: EdgeInsets.only(left: screenHeight * 0.025),
            child: const Text(
              "Rôle",
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
              textAlign: TextAlign.left,
            ),
          ),
          //Dropdown button for role
          DropdownButtonHideUnderline(
            child: Container(
              padding: const EdgeInsets.all(0.0),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.blueAccent),
                borderRadius: BorderRadius.circular(8),
              ),
              width: screenWidth * 0.95,
              margin: const EdgeInsets.all(10.0),
              child: DropdownButton<String>(
                value: selectedOption,
                isExpanded: true,
                icon: const Icon(
                  Icons.arrow_drop_down,
                  color: Colors.black,
                  size: 36,
                ),
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
                      child: Text(value,
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          )),
                    ),
                  );
                }).toList(),
              ),
            ),
          ),

          // add benevole button
          ButtonBar(
            alignment: MainAxisAlignment.center,
            buttonPadding: EdgeInsets.symmetric(horizontal: 16.0),
            children: [
              ElevatedButton(
                onPressed: () async {
                  setState(() {
                    _isLoading = true;
                  });
                  try {
                    String message = await VolunteerService().postVolunteer(
                        Config.cafeName, _controller.text, selectedOption);

                    // pop up message
                    print(message);
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        behavior: SnackBarBehavior.floating,
                        backgroundColor: Colors.blue,
                        content: Text(message,
                            style: const TextStyle(color: Colors.white)),
                        duration:
                            const Duration(seconds: 4), // Durée du SnackBar
                      ),
                    );
                  } catch (e) {
                    print("Failed to post volunteer: $e");
                    // pop up message
                    if (!mounted) {
                      return;
                    }
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text("Failed to post volunteer: $e",
                            style: const TextStyle(color: Colors.white)),
                        duration: const Duration(seconds: 4),
                        behavior: SnackBarBehavior.floating,
                        backgroundColor: Colors.red, // Durée du SnackBar
                      ),
                    );
                  } finally {
                    setState(() {
                      _isLoading = false;
                    });
                  }
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue, // Couleur de fond du bouton
                  foregroundColor: Colors.white, // Couleur du texte du bouton
                  padding:
                      EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
                  textStyle:
                      TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                child: const Text('Ajouter'),
              ),
            ],
          ),

          if (_isLoading) const Center(child: CircularProgressIndicator()),

          // delete text button
          ButtonBar(
            alignment: MainAxisAlignment.center,
            buttonPadding: EdgeInsets.symmetric(horizontal: 16.0),
            children: [
              ElevatedButton(
                onPressed: () {
                  _controller.clear();
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red, // Couleur de fond du bouton
                  foregroundColor: Colors.white, // Couleur du texte du bouton
                  padding:
                      EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
                  textStyle:
                      TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                child: const Text('Effacer tout'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
