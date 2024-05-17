package LimitOrderBookJAVA;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.HashMap;
import java.util.Comparator;

public class OrderBook {

    PriorityQueue<Order> sellOrders;
    PriorityQueue<Order> buyOrders;
    HashMap<Double, Integer> priceVolume;
    Comparator<Order> sellOrderComparator;
    Comparator<Order> buyOrderComparator;


    public OrderBook(){

        sellOrders = new PriorityQueue<>(sellOrderComparator);
        buyOrders = new PriorityQueue<>(Collections.reverseOrder());
        priceVolume = new HashMap<>();
        sellOrderComparator = Comparator
                .comparing(Order::getPrice)
                .thenComparing(Order::getOrderTime);
        buyOrderComparator = Comparator
                .comparing(Order::getPrice)
                .reversed()
                .thenComparing(Order::getOrderTime);
    }

    public void placeSellOrder(Order order){
        if (buyOrders.isEmpty()){
            addOrder(order);
            updatePriceVolume(order);
        }
    }

    private void updatePriceVolume(Order order){
        double price = order.getPrice();
        int volume = order.getVolume();
        if (priceVolume.containsKey(price)){
            int currentVolume = priceVolume.get(price);
            priceVolume.put(price, currentVolume + volume);
        } else{
            priceVolume.put(price, volume);
        }
    }

    public void placeBuyOrder(Order order){
        if (sellOrders.isEmpty()){
            addOrder(order);
            return;
        }
    }

    private void addOrder(Order order){
        if(order.getSide() == Order.Side.BUY){
            buyOrders.add(order);
        }else{
            sellOrders.add(order);
        }
    }
    
}
