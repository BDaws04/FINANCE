package LimitOrderBookJAVA;

public interface OrderBookINTERFACE {

    public void placeOrder(Order order);

    public void cancelOrder(int orderId);

    public void getVolumeAtPrice(double price);

}
