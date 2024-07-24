import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';

class NotificationItem {
  final String title;
  final String subtitle;

  NotificationItem(this.title, this.subtitle);
}

class AlertNotificationWidget extends StatefulWidget {
  final List<String> listOfProductsName;

  const AlertNotificationWidget({
    super.key,
    required this.listOfProductsName,
  });

  @override
  State<AlertNotificationWidget> createState() =>
      _AlertNotificationWidgetState();
}

class _AlertNotificationWidgetState extends State<AlertNotificationWidget> {
  List<PopupMenuItem<NotificationItem>> createPopupMenuItems() {
    String notificationText = "";
    return widget.listOfProductsName.map((item) {
      notificationText = AppLocalizations.of(context)!.low_stock_message(item);
      return PopupMenuItem<NotificationItem>(
        value: NotificationItem(item, notificationText),
        child: ListTile(
          leading: const Icon(Icons.article),
          title: Text(item,
              style:
                  const TextStyle(color: Color.fromARGB(255, 138, 199, 249))),
          tileColor: Colors.white,
          subtitle: Text(notificationText),
        ),
      );
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: <Widget>[
        IconButton(
          icon: const Icon(
            Icons.notifications,
            size: 25,
          ),
          onPressed: () {
            // Afficher le menu de notifications
            showMenu(
              context: context,
              position: const RelativeRect.fromLTRB(150.0, 150.0, 0.0, 0.0),
              color: Colors.white,
              items: <PopupMenuEntry<NotificationItem>>[
                ...createPopupMenuItems(),
              ],
            );
          },
        ),
        if (widget.listOfProductsName.isNotEmpty)
          Positioned(
            right: 6,
            top: 6,
            child: Container(
              padding: const EdgeInsets.all(2),
              decoration: BoxDecoration(
                color: Colors.red,
                borderRadius: BorderRadius.circular(10),
              ),
              constraints: const BoxConstraints(
                minWidth: 10,
                minHeight: 10,
              ),
              child: Text(
                '${widget.listOfProductsName.length}',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 12,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
      ],
    );
  }
}
