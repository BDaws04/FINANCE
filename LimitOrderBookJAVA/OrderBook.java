package LimitOrderBookJAVA;
import java.util.ArrayList;
import java.util.PriorityQueue;
import LimitOrderBookJAVA.Order.Side;
import java.util.HashMap;
import java.util.Comparator;
import java.util.Iterator;


public class OrderBook implements OrderBookINTERFACE {

    private PriorityQueue<Order> sellOrders;
    private PriorityQueue<Order> buyOrders;
    private HashMap<Double, Integer> buyVolume;
    private HashMap<Double, Integer> sellVolume;
    private Comparator<Order> sellOrderComparator;
    private Comparator<Order> buyOrderComparator;
    private ArrayList<Order> orders;


    public OrderBook(){

        sellOrderComparator = Comparator
                .comparing(Order::getPrice)
                .thenComparing(Order::getOrderTime);
        buyOrderComparator = Comparator
                .comparing(Order::getPrice)
                .reversed()
                .thenComparing(Order::getOrderTime);

        sellOrders = new PriorityQueue<>(sellOrderComparator);
        buyOrders = new PriorityQueue<>(buyOrderComparator);
        buyVolume = new HashMap<>();
        sellVolume = new HashMap<>();
        orders = new ArrayList<>();
      
    }

    public void getVolumeAtPrice(double price){
        int buyVolumeAtPrice = 0;
        int sellVolumeAtPrice = 0;

        if (buyVolume.containsKey(price)){
            buyVolumeAtPrice = buyVolume.get(price); 
        }
        if (sellVolume.containsKey(price)){
            sellVolumeAtPrice = sellVolume.get(price);
        }
        System.out.println("The buy volume at price: £" + price + " is " + buyVolumeAtPrice);
        System.out.println("The sell volume at price: £" + price + " is " + sellVolumeAtPrice);
    }

    public void placeOrder(Order order){

        if (order.getSide() == Side.BUY){
            placeBuyOrder(order);
        }
        else{
            placeSellOrder(order);
        }

    }

    private void placeBuyOrder(Order order){
        // if there are no sell orders in the market, add the buy order to the book
        if (sellOrders.isEmpty()){
            buyOrders.add(order);
            if (buyVolume.containsKey(order.getPrice())){
                int oldVolume = buyVolume.get(order.getPrice());
                buyVolume.put(order.getPrice(),oldVolume + order.getVolume());
            }
            else {
                buyVolume.put(order.getPrice(), order.getVolume());
            }
        }
        else if (order.getVolume() == 0){
            return;
        }
        else {
            Order sellOrderTop = sellOrders.peek();

            // if the cheapest selling price is greater than the buying price, order is added to the book
            if (sellOrderTop.getPrice() > order.getPrice()){
                buyOrders.add(order);
                
                if (buyVolume.containsKey(order.getPrice())){
                    int oldVolume = buyVolume.get(order.getPrice());
                    buyVolume.put(order.getPrice(),oldVolume + order.getVolume());
                }
                else {
                    buyVolume.put(order.getPrice(), order.getVolume());
                }
            }
            // a trade can now happen 
            // checks if all the volume can be removed it one go, else it will use recursion to complete the trade
            else {
                Order sellOrderTopR = sellOrders.poll();
                if (sellOrderTopR.getVolume() > order.getVolume()){
                    double price = sellOrderTopR.getPrice();
                    int volume = order.getVolume();
                    sellOrderTopR.setVolume(sellOrderTopR.getVolume() - volume);

                    int oldVolume = sellVolume.get(price);
                    sellVolume.put(price, oldVolume - volume);

                    sellOrders.add(sellOrderTopR);

                    System.out.println("User named: " + order.getClient() + " purchased " + volume + " at price: £" + price);

                }
                // completes the scenario when the top doesnt have enough volume
                else {

                    int availableVolume = sellOrderTopR.getVolume();
                    order.setVolume(order.getVolume() - availableVolume);

                    int oldVolume = sellVolume.get(sellOrderTopR.getPrice());
                    sellVolume.put(sellOrderTopR.getPrice(), oldVolume - availableVolume);
                    System.out.println("User named: " + order.getClient() + " purchased " + availableVolume + " at price: £" + sellOrderTopR.getPrice());

                    placeBuyOrder(order);

                }
            }
        }

    }

    private void placeSellOrder(Order order){
        // case where there is no buy orders in the market
        if (buyVolume.isEmpty()){
            sellOrders.add(order);
            if (sellVolume.containsKey(order.getPrice())){
                int oldVolume = sellVolume.get(order.getPrice());
                sellVolume.put(order.getPrice(),oldVolume + order.getVolume());
            }
            else {
                sellVolume.put(order.getPrice(), order.getVolume());
            }

        }
        // case where the user wants to sell 0 volume
        else if (order.getVolume() == 0){
            return;
        }
        else {

            Order buyOrderTop = buyOrders.peek();

            // case where no one wants to buy at that price 
            if (buyOrderTop.getPrice() < order.getPrice()){
                sellOrders.add(order);
                
                if (sellVolume.containsKey(order.getPrice())){
                    int oldVolume = sellVolume.get(order.getPrice());
                    sellVolume.put(order.getPrice(),oldVolume + order.getVolume());
                }
                else {
                    sellVolume.put(order.getPrice(), order.getVolume());
                }


            } else {
              Order buyOrderTopR = buyOrders.poll();
                if (buyOrderTopR.getVolume() > order.getVolume()){
                    double price = buyOrderTopR.getPrice();
                    int volume = order.getVolume();
                    buyOrderTopR.setVolume(buyOrderTopR.getVolume() - volume);

                    int oldVolume = buyVolume.get(price);
                    buyVolume.put(price, oldVolume - volume);

                    sellOrders.add(buyOrderTopR);
                    System.out.println("User named: " + buyOrderTopR.getClient() + " purchased " + order.getVolume() + " at price: £" + buyOrderTopR.getPrice());


                // may have to do multiple trades
                } else {
                    int availableVolume = buyOrderTopR.getVolume();
                    order.setVolume(order.getVolume() - availableVolume);

                    int oldVolume = buyVolume.get(buyOrderTopR.getPrice());
                    sellVolume.put(buyOrderTopR.getPrice(), oldVolume - availableVolume);
                    System.out.println("User named: " + buyOrderTopR.getClient() + " purchased " + availableVolume + " at price: £" + buyOrderTopR.getPrice());

                    placeSellOrder(order);

                }

            }

        }
    }

    public void cancelOrder(int orderId){
       Iterator<Order> iterator = orders.iterator();
       while (iterator.hasNext()) {
           Order order = iterator.next();
           if (order.getOrderId() == orderId) {

              int volume = order.getVolume();

               if (order.getSide() == Side.BUY){
                   buyOrders.remove(order);
                   int oldVolume = buyVolume.get(order.getPrice());
                   buyVolume.put(order.getPrice(), oldVolume - volume);
               }
               else {
                   sellOrders.remove(order);
                   int oldVolume = sellVolume.get(order.getPrice());
                   sellVolume.put(order.getPrice(), oldVolume - volume);
               }
               iterator.remove();
               System.out.println("Order has been removed");
           }
       }
       System.out.println("Order does not exist, or has already been executed");
}

}



   
   

  

   
      

   
    

