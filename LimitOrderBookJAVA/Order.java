package LimitOrderBookJAVA;
import java.time.LocalDateTime;
import java.time.ZoneOffset;


public class Order{

    public enum Side{
        BUY,
        SELL
    }
    private Side side;
    private final int orderId;
    private final String client;
    private double price;
    private int volume;
    private final LocalDateTime orderTime;

    // constructor for an order in the order book
     
    public Order(Side side, int orderId, String client, double price, int volume){
        this.side = side;
        this.orderId = orderId;
        this.client = client;
        this.price = price;
        this.volume = volume;
        orderTime = LocalDateTime.now(ZoneOffset.UTC);
    
    }

    // Getters and Setters for the variables of the orders

    public Side getSide(){
        return side;
    }

    public int getOrderId(){
        return orderId;
    }

    public String getClient(){
        return client;
    }

    public double getPrice(){
        return price;
    }
    public void setPrice(double price){
        this.price = price;
    }

    public int getVolume(){
        return volume;
    }
    public void setVolume(int volume){
        this.volume = volume;
    }

    public LocalDateTime getOrderTime(){
        return orderTime;
    }
}