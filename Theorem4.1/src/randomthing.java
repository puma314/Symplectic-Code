class randomthing 
{
	
	
	public static void main(String[] args) 
    {
		
		int myint = 10;
		int base = 3;
		for(int k=0; k <= myint; k++)
			System.out.println(function(k,base));
    }
	
    public static double function(int n, int m)
    {
    	if(n == 0)
    		return 1; 
    	if (m == 0)
    		return 1;
    	if (n == 1)
    		return 1;
    	
    	double finalsum=0;
    	
    	for (int k =2; k <= n; k++)
    	{
    		
    		double sum=0; 
    		
    		for(int i=1; i <= m; i++)
    		{
    			sum = sum + Math.pow(-1, m-i) * function(k, i-1);
    		}

    		finalsum = finalsum + function(n-k, m) * sum ;


    	}
    	
		finalsum = finalsum + function(n-1, m);

    	
    	return finalsum;
    }
}