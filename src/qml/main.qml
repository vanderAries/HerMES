import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.15
import "controls"

Window {
    id: mainWindow
    width: 1000
    height: 700
    minimumWidth: 800
    minimumHeight: 500
    visible: true
    color: "#00000000"
    title: qsTr("HerMES")

    // REMOVE TITLE BAR
    flags: Qt.Window | Qt.FramelessWindowHint

    // PROPERTIES
    property int windowStatus: 0
    property int windowMargin: 10

    // INTERNAL FUNCTIONS
    QtObject{
        id: internal
        function resetResizeBorders(){
            // RESIZE VISIBILITY
            resizeLeft.visible = true
            resizeRight.visible = true
            resizeBottom.visible = true
            resizeCorner.visible = true
        }

        function maximizeRestore(){
            if(windowStatus == 0){
                mainWindow.showMaximized()
                windowStatus = 1
                windowMargin = 0
                // RESIZE VISIBILITY
                resizeLeft.visible = false
                resizeRight.visible = false
                resizeBottom.visible = false
                resizeCorner.visible = false
                btnMaximizeRestore.btnIconSource = "../images/svg_images/restore_icon.svg"
            }
            else{
                mainWindow.showNormal()
                windowStatus = 0
                windowMargin = 10
                // RESIZE VISIBILITY
                internal.resetResizeBorders()
                btnMaximizeRestore.btnIconSource = "../images/svg_images/maximize_icon.svg"
            }
        }

        function ifMaximizedWindowRestore(){
            if(windowStatus == 1){
                mainWindow.showNormal()
                windowStatus = 0
                windowMargin = 10
                // RESIZE VISIBILITY
                internal.resetResizeBorders()
                btnMaximizeRestore.btnIconSource = "../images/svg_images/maximize_icon.svg"
            }
        }

        function restoreMargins(){
            windowStatus = 0
            windowMargin = 10
            // RESIZE VISIBILITY
            internal.resetResizeBorders()
            btnMaximizeRestore.btnIconSource = "../images/svg_images/maximize_icon.svg"
        }

    }



    Rectangle {
        id: bg
        visible: true
        color: "#2d3439"
        border.color: "#3d464b"
        border.width: 1
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: windowMargin
        anchors.leftMargin: windowMargin
        anchors.bottomMargin: windowMargin
        anchors.topMargin: windowMargin
        z: 1

        Rectangle {
            id: appContainer
            color: "#00000000"
            anchors.fill: parent
            anchors.rightMargin: 1
            anchors.leftMargin: 1
            anchors.bottomMargin: 1
            anchors.topMargin: 1

            Rectangle {
                id: topBar
                height: 60
                color: "#1b1f22"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.topMargin: 0

                MenuButton {
                    btnColorClicked: "#ce4500"
                    onClicked: animationMenu.running = true

                }

                Rectangle {
                    id: topBarDescription
                    y: 133
                    height: 25
                    color: "#282e32"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 70
                    anchors.bottomMargin: 0

                    Label {
                        id: labelTopInfo
                        color: "#9ca7b3"
                        text: qsTr("Finite Element Method Solver for truss structures")
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        verticalAlignment: Text.AlignVCenter
                        anchors.leftMargin: 10
                        anchors.rightMargin: 300
                    }

                    Label {
                        id: labelRightInfo
                        color: "#9ca7b3"
                        text: qsTr("Version 1.1.0")
                        anchors.left: labelTopInfo.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        horizontalAlignment: Text.AlignRight
                        verticalAlignment: Text.AlignVCenter
                        anchors.leftMargin: 0
                        anchors.rightMargin: 10
                    }
                }

                Rectangle {
                    id: titleBar
                    y: 133
                    height: 35
                    color: "#00000000"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 70
                    anchors.rightMargin: 105
                    anchors.bottomMargin: 25

                    DragHandler{
                        onActiveChanged: if(active){
                                             mainWindow.startSystemMove()
                                             internal.ifMaximizedWindowRestore()
                                         }
                    }

                    Image {
                        id: iconApp
                        width: 50
                        // height: 22
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        source: "../images/icon_app.png"
                        anchors.leftMargin: 5
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        fillMode: Image.PreserveAspectFit
                    }

                    Label {
                        id: labelAppName
                        color: "#deedff"
                        text: qsTr("HerMES")
                        anchors.left: iconApp.right
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 10
                        anchors.leftMargin: 5
                    }
                }

                Row {
                    id: rowBtns
                    x: 528
                    y: 0
                    width: 105
                    height: 35
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.rightMargin: 0
                    anchors.topMargin: 0

                    TopBarButton{
                        id: btnMinimize
                        btnColorClicked: "#ce4500"
                        onClicked: {
                            mainWindow.showMinimized()
                            internal.restoreMargins()
                        }
                    }

                    TopBarButton {
                        id: btnMaximizeRestore
                        btnColorClicked: "#ce4500"
                        btnIconSource: "../images/svg_images/maximize_icon.svg"
                        onClicked: internal.maximizeRestore()

                    }

                    TopBarButton {
                        id: btnClose
                        btnColorMouseOver: "#be0000"
                        btnColorClicked: "#2d3439"
                        btnIconSource: "../images/svg_images/close_icon.svg"
                        onClicked: mainWindow.close()
                    }
                }
            }

            Rectangle {
                id: content
                color: "#00000000"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: topBar.bottom
                anchors.bottom: parent.bottom
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.bottomMargin: 0
                anchors.topMargin: 0

                Rectangle {
                    id: leftMenu
                    width: 70
                    color: "#1b1f22"
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0

                    PropertyAnimation{
                        id: animationMenu
                        target: leftMenu
                        property: "width"
                        to: if(leftMenu.width == 70) return 170; else return 70
                        duration: 300
                        easing.type: Easing.InOutQuint
                    }

                    Column {
                        id: columnMenus
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 0
                        anchors.leftMargin: 0
                        anchors.bottomMargin: 90
                        anchors.topMargin: 0

                        LeftMenuBtn {
                            id: btnModel
                            width: leftMenu.width
                            opacity: 0.8
                            text: qsTr("Model")
                            iconWidth: 25
                            iconHeight: 25
                            btnIconSource: "../images/svg_images/molecular-structure.svg"
                            btnColorMouseOver: "#2b3136"
                            isActiveMenu: true
                            onClicked: {
                                btnModel.isActiveMenu = true
                                btnSolve.isActiveMenu = false
                                btnExamples.isActiveMenu = false
                                btnExport.isActiveMenu = false
                                btnSettings.isActiveMenu = false
                                pageModel.visible = true
                                pageSolve.visible = false
                                pageExamples.visible = false
                                pageExport.visible = false
                                pageSettings.visible = false
                            }
                        }

                        LeftMenuBtn {
                            id: btnSolve
                            width: leftMenu.width
                            opacity: 0.8
                            text: qsTr("Solve")
                            iconWidth: 22
                            iconHeight: 22
                            btnIconSource: "../images/svg_images/balance-sheet.svg"
                            btnColorMouseOver: "#2b3136"
                            isActiveMenu: false
                            onClicked: {
                                btnModel.isActiveMenu = false
                                btnSolve.isActiveMenu = true
                                btnExamples.isActiveMenu = false
                                btnExport.isActiveMenu = false
                                btnSettings.isActiveMenu = false
                                pageModel.visible = false
                                pageSolve.visible = true
                                pageExamples.visible = false
                                pageExport.visible = false
                                pageSettings.visible = false

                            }
                        }

                        LeftMenuBtn {
                            id: btnExamples
                            width: leftMenu.width
                            opacity: 0.8
                            visible: true
                            text: qsTr("Examples")
                            iconWidth: 20
                            iconHeight: 20
                            btnIconSource: "../images/svg_images/list.svg"
                            btnColorMouseOver: "#2b3136"
                            onClicked: {
                                btnModel.isActiveMenu = false
                                btnSolve.isActiveMenu = false
                                btnExamples.isActiveMenu = true
                                btnExport.isActiveMenu = false
                                btnSettings.isActiveMenu = false
                                pageModel.visible = false
                                pageSolve.visible = false
                                pageExamples.visible = true
                                pageExport.visible = false
                                pageSettings.visible = false
                            }
                        }

                        LeftMenuBtn {
                            id: btnImport
                            width: leftMenu.width
                            opacity: 0.8
                            text: qsTr("Import")
                            btnIconSource: "../images/052-inside.png"
                            btnColorMouseOver: "#2b3136"
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


                        LeftMenuBtn {
                            id: btnExport
                            width: leftMenu.width
                            opacity: 0.8
                            text: qsTr("Export")
                            btnIconSource: "../images/061-outside.png"
                            btnColorMouseOver: "#2b3136"
                            onClicked: {
                                btnModel.isActiveMenu = false
                                btnSolve.isActiveMenu = false
                                btnExamples.isActiveMenu = false
                                btnExport.isActiveMenu = true
                                btnSettings.isActiveMenu = false
                                pageModel.visible = false
                                pageSolve.visible = false
                                pageExamples.visible = false
                                pageExport.visible = true
                                pageSettings.visible = false
                            }
                        }


                    }

                    LeftMenuBtn {
                        id: btnSettings
                        x: 0
                        y: 314
                        width: leftMenu.width
                        text: qsTr("Settings")
                        anchors.bottom: parent.bottom
                        clip: true
                        anchors.bottomMargin: 25
                        btnIconSource: "../images/svg_images/settings_icon.svg"
                        btnColorMouseOver: "#2b3136"
                        onClicked: {
                            btnModel.isActiveMenu = false
                            btnSolve.isActiveMenu = false
                            btnExamples.isActiveMenu = false
                            btnExport.isActiveMenu = false
                            btnSettings.isActiveMenu = true
                            pageModel.visible = false
                            pageSolve.visible = false
                            pageExamples.visible = false
                            pageExport.visible = false
                            pageSettings.visible = true
                        }
                    }
                }

                Rectangle {
                    id: contentPages
                    color: "#2d3439"
                    anchors.left: leftMenu.right
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    clip: true
                    anchors.topMargin: 0
                    anchors.bottomMargin: 25
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0

                    Loader{
                        id: pageModel
                        anchors.fill: parent
                        source: Qt.resolvedUrl(("pages/modelPage.qml"))
                        visible: true
                    }
                    Loader{
                        id: pageSolve
                        anchors.fill: parent
                        source: Qt.resolvedUrl("pages/solvePage.qml")
                        visible: false
                    }
                    Loader{
                        id: pageExamples
                        anchors.fill: parent
                        source: Qt.resolvedUrl("pages/examplesPage.qml")
                        visible: false
                    }
                    Loader{
                        id: pageSettings
                        anchors.fill: parent
                        source: Qt.resolvedUrl("pages/settingsPage.qml")
                        visible: false
                    }
                    Loader{
                        id: pageExport
                        anchors.fill: parent
                        source: Qt.resolvedUrl("pages/exportPage.qml")
                        visible: false
                    }
                }


                Rectangle {
                    id: rectangle
                    color: "#272c30"
                    anchors.left: leftMenu.right
                    anchors.right: parent.right
                    anchors.top: contentPages.bottom
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 0
                    anchors.topMargin: 0
                    anchors.rightMargin: 0

                    MouseArea {
                        id: resizeCorner
                        x: 894
                        y: 11
                        width: 35
                        height: 35
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: -10
                        cursorShape: Qt.SizeFDiagCursor
                        anchors.bottomMargin: -10

                        Image {
                            id: image
                            opacity: 0.7
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            source: "../images/svg_images/resize_icon.svg"
                            anchors.topMargin: 5
                            anchors.leftMargin: 5
                            anchors.rightMargin: 10
                            anchors.bottomMargin: 10
                            sourceSize.height: 16
                            sourceSize.width: 16
                            fillMode: Image.PreserveAspectFit
                            antialiasing: false
                        }

                        DragHandler{
                            target: null
                            onActiveChanged: if (active) {mainWindow.startSystemResize(Qt.RightEdge | Qt.BottomEdge)}
                        }


                    }

                    RowLayout {
                        id: rowLayout
                        width: 400
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.leftMargin: 10

                        Text {
                            id: geometryStatus
                            color: "#ffffff"
                            text: qsTr("Data not imported")
                            font.pixelSize: 12
                            Layout.bottomMargin: 15
                            clip: false
                            Layout.fillHeight: false
                            Layout.fillWidth: false
                        }

                        CustomRadioButton {
                            id: geomStatusBox
                            text: "RadioButton"
                            Layout.topMargin: -3
                            Layout.bottomMargin: 10
                            colorDisabled: "#881111"
                            checked: true
                            setText: ""
                            checkable: false
                            colorTextDisabled: "#ffffff"
                        }

                        Text {
                            id: buildStatus
                            color: "#ffffff"
                            text: qsTr("Model not built")
                            font.pixelSize: 12
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                            Layout.bottomMargin: 15
                            Layout.fillHeight: false
                            Layout.fillWidth: false
                        }

                        CustomRadioButton {
                            id: buildStatusBox
                            text: "RadioButton"
                            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                            Layout.bottomMargin: 10
                            Layout.topMargin: -3
                            Layout.fillHeight: false
                            Layout.fillWidth: false
                            setText: ""
                            colorTextDisabled: "#ffffff"
                            checked: true
                            colorDisabled: "#881111"
                            checkable: false
                        }

                        Text {
                            id: resultsStatus
                            color: "#ffffff"
                            text: qsTr("Results not ready")
                            font.pixelSize: 12
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            Layout.bottomMargin: 15
                        }

                        CustomRadioButton {
                            id: resultsStatusBox
                            text: "RadioButton"
                            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                            Layout.topMargin: -3
                            Layout.bottomMargin: 10
                            colorTextDisabled: "#ffffff"
                            setText: ""
                            checked: true
                            colorDisabled: "#b08a03"
                            checkable: false
                        }
                    }





                }
            }
        }
    }


    DropShadow{
        anchors.fill: bg
        horizontalOffset: 0
        verticalOffset: 0
        radius: 10
        samples: 16
        color: "#80000000"
        source: bg
        z: 0
    }

    MouseArea {
        id: resizeLeft
        width: 10
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 0
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        cursorShape: Qt.SizeHorCursor

        DragHandler{
            target: null
            onActiveChanged: if (active) {mainWindow.startSystemResize(Qt.LeftEdge)}
        }
    }

    MouseArea {
        id: resizeRight
        width: 10
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.bottomMargin: 35
        anchors.topMargin: 10
        cursorShape: Qt.SizeHorCursor

        DragHandler{
            target: null
            onActiveChanged: if (active) {mainWindow.startSystemResize(Qt.RightEdge)}
        }
    }

    MouseArea {
        id: resizeBottom
        height: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: 10
        anchors.bottomMargin: 0
        anchors.rightMargin: 35
        cursorShape: Qt.SizeVerCursor

        DragHandler{
            target: null
            onActiveChanged: if (active) {mainWindow.startSystemResize(Qt.BottomEdge)}
        }
    }

    Connections {
        target: backend

        function onIsDataLoaded(dataImported){
            geometryStatus.text = qsTr(dataImported)
            geomStatusBox.colorDisabled = "#12a51c"

            buildStatus.text = qsTr("Model not built")
            buildStatusBox.colorDisabled = "#881111"

            resultsStatus.text = qsTr("Results not ready")
            resultsStatusBox.colorDisabled = "#b08a03"
        }

        function onIsModelBuilt(modelBuilt){
            buildStatus.text = qsTr(modelBuilt)
            buildStatusBox.colorDisabled = "#12a51c"
        }

        function onIsResultsReady(resultsReady){
            resultsStatus.text = qsTr(resultsReady)
            resultsStatusBox.colorDisabled = "#12a51c"
        }
    }
}


/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}D{i:38}
}
##^##*/
