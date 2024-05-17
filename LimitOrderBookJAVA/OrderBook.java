package LimitOrderBookJAVA;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.HashMap;

public class OrderBook {

    PriorityQueue<Order> sellOrders;
    PriorityQueue<Order> buyOrders;
    HashMap<Double, Integer> priceVolume;


    public OrderBook(){
        sellOrders = new PriorityQueue<>();
        buyOrders = new PriorityQueue<>(Collections.reverseOrder());
        priceVolume = new HashMap<>();
    }

    public void placeSellOrder(Order order){
        if (buyOrders.isEmpty()){
            double price = order.getPrice();
            int volume = order.getVolume();
            if (priceVolume.containsKey(price)){
                int currentVolume = priceVolume.get(price);
                priceVolume.put(price, currentVolume + volume);
            } else{
                priceVolume.put(price, volume);
            }
            addOrder(order);
        }
    }

    public void placeBuyOrder(Order order){
        if (sellOrders.isEmpty()){
            addOrder(order);
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
