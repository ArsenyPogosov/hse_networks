# Лаболаторная работа 1.

### Топология
![](img/topology.png)

### Настройка компонент
* VPC1
  
  ![](img/vpc1.png)

* VPC2

  ![](img/vpc2.png)

* Switch3

  ![](img/switch3.png)

* Switch4

  ![](img/switch4.png)

* Switch5

  ![](img/switch5.png)

* vIOS

  ![](img/vIOS.png)

### Пинги между VPC
![](img/ping_12_full_top.png)

![](img/ping_21_full_top.png)

### Проверка заблокированности линка
* Spanning tree у Switch4:

  ![](img/spann_4.png)

* Линк между Switch4 и Switch3 действительно заблокировался

### Отказоустойчивость

* Выключаем интерфейс Gi0/2 у Switch3

  ![](img/switch3_link_shutdown.png)

* Проверяем пинги

  ![](img/ping_12_link_shutdown.png)

  ![](img/ping_21_link_shutdown.png)
