import 'package:flutter/material.dart';

class NotificationItem {
  final String title;
  final String subtitle;

  NotificationItem(this.title, this.subtitle);
}

class AlertNotificationWidget extends StatefulWidget {
  final List<List<String>> popupMenuItem;

  const AlertNotificationWidget({
    super.key,
    required this.popupMenuItem,
  });

  @override
  State<AlertNotificationWidget> createState() =>
      _AlertNotificationWidgetState();
}

class _AlertNotificationWidgetState extends State<AlertNotificationWidget> {
  List<PopupMenuItem<NotificationItem>> createPopupMenuItems() {
    return widget.popupMenuItem
        .map((item) => PopupMenuItem<NotificationItem>(
              value: NotificationItem(item[0], item[1]),
              child: ListTile(
                leading: const Icon(Icons.article),
                title: Text(item[0]),
                subtitle: Text(item[1]),
              ),
            ))
        .toList();
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
              items: <PopupMenuEntry<NotificationItem>>[
                ...createPopupMenuItems(),
              ],
            );
          },
        ),
        if (widget.popupMenuItem.isNotEmpty)
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
                '${widget.popupMenuItem.length}',
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
