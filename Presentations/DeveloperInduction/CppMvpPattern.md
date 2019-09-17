# MVP Pattern in C++

This tutorial covers a basic implementation of the Model-View-Presenter (MVP) pattern in C++ using Qt. The MVP pattern is the standard in Mantid for creating GUIs.

Setup
-----

The quickest way to get started is by using the Qt extension to visual studio.

First create a new project *File->New->Project*, go to the Qt menu and select Qt Application GUI. Change the *Name* and *Solution name* to "MVP_Tutorial_1". A window should appear, click next and on the second window make sure the *Gui*, *Core* and *Widget* modules are ticked. Leave everything else as its default. You will now see various files in the solution explorer.

The ".ui" files are a Qt type which can be opened with Qt Designer; with the Qt extension in visual studio you should be able to double click these files to automatically open them with Designer. First we will create the look of our basic widget, so right click on the *Form Files* folder and select *Add->New Item*, select "Qt Widget Form File" from the Qt menu. Call the file "dummywidget.ui".

Double click the file to open Qt Designer.

Producing the widget ui file
----------------------------

Right click the `Form Files` folder and select Add->New Item, then ....

...

When the project is build, Qt will generate a header file called "ui_dummwidget.h" which defines a class `Ui_DummyWidget`.

The view
--------

We will now create the *view* for our widget. The view is responsible for the layout and appearance of the interface; it pieces together all the widgets (buttons, boxes, displays etc.) and defines basic signals such as button presses and user editing. From a code perspective it should be the only class which contains any reference to Qt. You may see connections between signals and slots, but only implementing fairly simple functionality, anything which requires more complex manipulation of data will be left for the model; we just define the signals which the view will emit to signify that actions need to be taken by the model (this are connected to slots via the presenter).

Add a new header file called `dummyview.h`.

```C++
#ifndef DUMMYVIEW_H
#define DUMMYVIEW_H

#include <string>
#include "ui_dummywidget.h"


class DummyView : public QWidget {
  Q_OBJECT

public:
  explicit DummyView(QWidget *parent = 0);
  ~DummyView();

  void setLabelText(const std::string &text);
  std::string getUserText();

private slots:
  void onPushButtonClicked();

private:
  Ui::DummyWidget *ui;
};

#endif // DUMMYVIEW_H
```

The view acts as a widget, so it must inherit from `QWidget`, we add the standard `QObject` macro which all widgets must have (it allows the sandards definitions of signals and slots for one thing). The constructor must allow us to pass the parent widget if one exists.

Our GUI has a label for which we can set the text, so we define a public method to do that (so that the presenter can use it). We also create a method to extract the text entered by the user from the text box.

Observer/Subscriber
--------------------

Let's consider what to do with the `onPushButtonClicked()` slot. Unsurprisingly, this slot responds to the user clicking the button. We want this slot to do two things; grab the user input, and after manipulating that text place it back into the label to be displayed in the GUI. This is pretty simple, and could be implemented directly in `dummyview.cpp`; however this would break the MVP pattern (especially if the required action was more complicated). The action we want this slot to take should be implemented in the *model*, which is separated from the view by the *presenter*, so we need to communicate to the presenter.

A simple way to do this is to define a new signal in the view. Let's be really explicit and call this new signal `userHasPressedButton`. It would be defined in the view class as

```C++
signals:
    void userHasPressedButton();
```

Then our implementation would be

```C++
void DummyView::onPushButtonClicked()
{
    emit userHasPressedButton();
}
```

Then the presenter can simply connect this signal to a slot which communicates with the model. However this **is not** the best way to achieve the communication with the presenter, because it forces the presenter to know about Qt as it must implement a `connect` statement to connect the signal to a slot.

This motivates the use of a *subscriber* pattern.

...

The rewritten header file looks like,

```C++
// dummyview.h
#ifndef DUMMYVIEW_H
#define DUMMYVIEW_H

#include "dummyviewsubscriber.h"
#include <QWidget>
#include <string>
#include "ui_dummywidget.h"

class DummyView : public QWidget {
  Q_OBJECT

public:
  explicit DummyView(QWidget *parent = 0);
  virtual ~DummyView() = default;

  void subscribe(DummyViewSubscriber *subscriber);

  void setLabelText(const std::string &text);
  std::string getUserText();

private slots:
  void onPushButtonClicked();

private:
  DummyViewSubscriber *m_subscriber;
  Ui::DummyWidget *m_ui;
};

#endif // DUMMYVIEW_H
```

The view now holds a private member variable `m_subscriber`, a pointer to an instance of `DummyViewSubscriber` along with a method `subscribe` which takes a subscriber and sets it as `m_subscriber`;

```C++
// dummyview.cpp
void DummyView::subscribe(DummyViewSubscriber *subscriber) {
  m_subscriber = subscriber;
}
```

We now reimplement the slot

```C++
// dummyview.cpp
void DummyView::onPushButtonClicked() {
  m_subscriber->notifyButtonPressed();
}
```

Now we can see that the subscriber has a method `actionOnButtonPress()`.

The Subscriber
--------------

Below is the header file

```C++
// dummyviewsubscriber.h
#ifndef DUMMYVIEWSUBSCRIBER
#define DUMMYVIEWSUBSCRIBER

class DummyViewSubscriber {
public:
	virtual void notifyButtonPressed() = 0;
};

#endif
```

This is an absract base class, the usage of `virtual` indicates we with to use inheritance and polymorphism, and the `= 0` indicates a *pure virtual function* and therefore a *abstract base class* (for this reason we don't need a corresponding .cpp file). Our only requirement for a concrete subscriber is that is can handle the button press through the method `actionOnButtonPress()`. The subscriber knows nothing about the model.

The Model
---------

The model handles and underlying logic of the GUI. For our simple GUI the only processing needed is to convert the user input text into a message which can then be dsiplayed.


```C++
// dummymodel.h

#ifndef DUMMYMODEL_H
#define DUMMYMODEL_H

#include <string>

class DummyModel {
public:
    DummyModel() = default;
    std::string generateText(const std::string& name);
};

#endif // DUMMYMODEL_H
```
With a corresponding `.cpp` file;

```C++
// dummymodel.cpp

#include "dummymodel.h"
#include <string>

std::string DummyModel::generateText(const std::string& name) {
    return "Hello " + name + "!";
}
```

The Presenter
-------------

Now we have the view, the subscriber and model and we wish to allow the view/model to communicate via the *presenter*. The presenter should be a concrete implementation of the subscriber (using the conventional inheritance mnemonic the presenter **is a** subscriber) and so inherits our abstract base class `DummyViewSubscriber`. The presenter *subscribes* to the view, which is us asking for the presenter to be made aware of any changes occuring in the view, through the interface we define in the subscriber.

Recall that we defined only a single member of the subscriber `actionOnButtonPress()`; so we must implement that. In order to implement the method correctly the presenter must know about the view and model. Thus when we create an instance of the presenter it should accept a `DummyView` and `DummyModel` object. Let's write the header file;

```C++
// dummypresenter.h

#ifndef DUMMYPRESENTER_H
#define DUMMYPRESENTER_H

#include "dummymodel.h"
#include "dummyview.h"
#include "dummyviewsubscriber.h"
#include <memory>

class DummyPresenter : public DummyViewSubscriber {

public:
  DummyPresenter(std::unique_ptr<DummyView> view,
                 std::unique_ptr<DummyModel> model);

  void notifyButtonPressed() override;

private:
  std::unique_ptr<DummyModel> m_model;
  std::unique_ptr<DummyView> m_view;
};

#endif // DUMMYPRESENTER_H
```

We can see that the presenter is holding pointers to both the view and model through `m_view`, `m_model`. We can also see that the inherited virtual method `notifyButtonPressed` is being overriden (as it must be).

```C++
// dummypresenter.cpp
#include "dummypresenter.h"
#include "dummymodel.h"
#include "dummyview.h"

#include <utility>
#include <string>

DummyPresenter::DummyPresenter(std::unique_ptr<DummyView> view,
                               std::unique_ptr<DummyModel> model)
    : m_model(std::move(model)), m_view(std::move(view)) {
  m_view->subscribe(this);
}

void DummyPresenter::notifyButtonPressed() {
  std::string name = m_view->getUserText();
  std::string text = m_model->generateText(name);
  m_view->setLabelText(text);
}
```

We can see one important feature of the subscriber in the constructor `m_view->subscribe(this)`, which is the presenter (`this`) telling the view (the 'publisher') that it wants to subscribe to it.

Bringing it all together
------------------------

Now we have all the functionality in place, we can create our GUI in the `main` method

```C++
// main.cpp

#include "dummywidget.h"
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QMainWindow>
#include <memory>

std::pair<std::unique_ptr<DummyPresenter>, DummyView*>> createDummyWidget(QWidget *parent) {
  auto view = std::make_unique<DummyView>(parent);
  auto viewPtr = view.get();
  auto model = std::make_unique<DummyModel>();
  auto presenter = std::make_unique<DummyPresenter>(std::move(view), std::move(model));

  // NOTE: viewPtr remains valid even though view is moved, this is because it is a
  //       pointer to the object on the heap, not to unique_ptr itself.
  //       doing view.get() in the call to make_pair would however,
  //       be undefined behaviour because the unique_ptr view has been moved and
  //       'use after move' is not supposed to be well-defined.

  return std::make_pair(std::move(presenter), viewPtr);
} // namespace

int main(int argc, char *argv[]) {

  QApplication a(argc, argv);

  QWidget *w = new QMainWindow();
  w->resize(400, 400);
  w->setObjectName(QStringLiteral("centralWidget"));
  auto gridLayout = new QGridLayout(w);
  gridLayout->setObjectName(QStringLiteral("gridLayout"));

  auto widget = createDummyWidget(w);
  gridLayout->addWidget(widget.second);

  w->show();
  return a.exec();
}
```

Discussing the `main` method here is beyond the scope of this tutorial, we are just interested in the `createDummyWidget` method. This method creates instances of the view and model as unique pointers and then feeds these into an instance of the presenter, returning the presenter and a non-owning pointer to the view.

Summary
-------

This tutorial outlines a "minimal example" of an implementation in C++ of the MVP pattern, and simple widget where a user enters text clicks a button and sees a formatted response in a label. It is not quite a minimal example, but the additional features which are present more strongly enforce the MVP pattern.

- The publisher/subscriber (aka observable/observer) pattern has been applied to the view/presenter to prevent any Qt code appearing in the presenter. This used the concepts of *abstract base classes* and *polymorphism*.

- The model/view/presenter are passed around as *unique pointers*. This enforces good/automatic memory management and clearer code.
