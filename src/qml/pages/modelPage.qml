import QtQuick 2.15
import QtQuick.Controls 2.15
import "../controls"
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.2

Item {
    id: item1
    property alias importBtn2Width: importBtn2.width

    Rectangle {
        id: rectangle
        color: "#2d3439"
        anchors.fill: parent


        Rectangle {
            id: rectangle2
            color: "#282e32"
            radius: 10
            anchors.left: parent.left
            anchors.right: parent.horizontalCenter
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 10
            anchors.bottomMargin: 10
            anchors.topMargin: 10
            anchors.rightMargin: 10
            Layout.fillWidth: true

            ColumnLayout {
                id: leftSide
                anchors.fill: parent

                ColumnLayout {
                    id: importLayout
                    width: 100
                    height: 100
                    spacing: 10
                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    Text {
                        id: text1
                        color: "#ffffff"
                        text: qsTr("IMPORT")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                        Layout.topMargin: 10
                        Layout.fillWidth: true
                        Layout.fillHeight: false
                    }

                    Text {
                        id: text2
                        color: "#ffffff"
                        text: qsTr("Import data file")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: false
                    }

                    RowLayout {
                        id: rowLayout
                        width: 100
                        height: 80
                        Layout.bottomMargin: 0
                        spacing: 15
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                        Layout.fillHeight: false
                        Layout.fillWidth: true

                        CustomButton {
                            id: importBtn2
                            text: qsTr("Import")
                            colorPressed: "#ce4500"
                            colorMouseOver: "#b46843"
                            colorDefault: "#66707b"
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                            Layout.leftMargin: 10
                            onClicked: {
                                fileImport.open()
                            }
                        }

                        FileDialog{
                            id: fileImport
                            title: "Choose data file"
                            selectMultiple: false
                            nameFilters: ["JSON (*.json)"]
                            onAccepted: {
                                backend.importFile(fileImport.fileUrl)
                            }
                        }

                        CustomTextField {
                            id: importPathField
                            Layout.rightMargin: 10
                            colorText: "#ffffff"
                            colorDefault: "#1b1f22"
                            colorMouseOver: "#202528"
                            colorOnFocus: "#363f44"
                            Layout.fillWidth: true
                            placeholderText: "File path"
                            onAccepted: {
                                backend.importFileFromPath(importPathField.text)
                            }
                        }
                    }
                }

                Rectangle {
                    id: rectangle5
                    height: 3
                    color: "#8599a6"
                    Layout.rightMargin: 5
                    Layout.leftMargin: 5
                    Layout.fillHeight: false
                    Layout.fillWidth: true

                }

                ColumnLayout {
                    id: buildLayout
                    width: 100
                    height: 100
                    spacing: 10
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Text {
                        id: text3
                        color: "#ffffff"
                        text: qsTr("BUILD")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                        Layout.fillWidth: true
                        Layout.fillHeight: false
                        Layout.topMargin: 0
                    }

                    RowLayout {
                        id: rowLayout2
                        width: 250
                        Layout.fillWidth: false
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom


                        Text {
                            id: text4
                            color: "#ffffff"
                            text: qsTr("Structure type:")
                            font.pixelSize: 12
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                            Layout.fillWidth: true
                            Layout.fillHeight: false
                        }

                        CustomRadioButton {
                            id: sTypeBtn2
                            property bool twoDim: false
                            text: "RadioButton"
                            colorDisabled: "#25282b"
                            colorTextDisabled: "#ffffff"
                            checked: sTypeBtn2.twoDim ? true : false
                            checkable: false
                            setText: "2D"
                        }

                        CustomRadioButton {
                            id: sTypeBtn3
                            property bool threeDim: false
                            text: "RadioButton"
                            colorTextDisabled: "#ffffff"
                            colorDisabled: "#25282b"
                            checked: sTypeBtn3.threeDim ? true : false
                            checkable: false
                            setText: "3D"
                        }

                    }

                    CustomButton {
                        id: buildModelBtn
                        text: qsTr("Build model")
                        Layout.preferredHeight: 30
                        Layout.preferredWidth: 100
                        Layout.fillHeight: false
                        colorPressed: "#ce4500"
                        colorMouseOver: "#b46843"
                        colorDefault: "#66707b"
                        Layout.fillWidth: false
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                        onClicked:
                            backend.buildModel()
                    }
                }

                Rectangle {
                    id: rectangle6
                    height: 3
                    color: "#8599a6"
                    Layout.rightMargin: 5
                    Layout.leftMargin: 5
                    Layout.fillHeight: false
                    Layout.fillWidth: true
                }


                ColumnLayout {
                    id: printLayout
                    width: 100
                    height: 100
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Text {
                        id: text5
                        color: "#ffffff"
                        text: qsTr("PRINT")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: false
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                        Layout.topMargin: 0
                    }

                    Text {
                        id: text6
                        color: "#ffffff"
                        text: qsTr("Show model preview in external window")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: false
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    }

                    CustomButton {
                        id: printModelBtn
                        text: qsTr("Print")
                        Layout.preferredHeight: 30
                        Layout.preferredWidth: 100
                        colorPressed: "#ce4500"
                        colorMouseOver: "#b46843"
                        colorDefault: "#66707b"
                        Layout.bottomMargin: 10
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                        onClicked: backend.printModel()

                    }
                }

            }

        }

        Rectangle {
            id: rectangle1
            x: 368
            width: 3
            color: "#8599a6"
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.topMargin: 10
            anchors.bottomMargin: 10
            anchors.horizontalCenter: parent.horizontalCenter
        }


        Rectangle {
            id: rectangle3
            x: 400
            y: 0
            color: "#282e32"
            radius: 10
            anchors.left: parent.horizontalCenter
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 10
            anchors.bottomMargin: 10
            anchors.topMargin: 10
            anchors.leftMargin: 10
            Layout.margins: 10

            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            Layout.fillHeight: true
            Layout.fillWidth: true

            ColumnLayout {
                id: rightSide
                anchors.fill: parent

                Text {
                    id: text7
                    color: "#ffffff"
                    text: qsTr("MODEL INFO")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    Layout.topMargin: 10
                    Layout.fillWidth: true
                    Layout.fillHeight: false
                }

                Flickable {
                    id: flickable
                    width: 300
                    height: 300
                    clip: true
                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    TextArea.flickable: TextArea {
                        id: modelInfoField
                        color: "#ffffff"
                        anchors.fill: parent
                        anchors.rightMargin: 20
                        readOnly: true
                        font.pointSize: 10
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        placeholderText: qsTr("")
                        selectByMouse: true
                        selectionColor: "#ce6835"
                    }

                    ScrollBar.vertical: ScrollBar{}
                }

            }
        }
    }

    Connections {
        target: backend

        function onReadPath(path){
            importPathField.text = path
        }

        function onReadModelInfo(info){
            modelInfoField.text = info
        }

        function onIs2D(bool){
            sTypeBtn2.twoDim = bool
            sTypeBtn3.threeDim = !bool
        }

        function onIs3D(bool){
            sTypeBtn3.threeDim = bool
            sTypeBtn2.twoDim = !bool
        }
    }
}




/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.1;height:480;width:800}
}
##^##*/
