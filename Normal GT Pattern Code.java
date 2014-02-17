
public class tstj 
{
	int tot, tot_ll, tot_rl, tot_spc;

	public tstj() 
	{
		tot = tot_ll = tot_rl = tot_spc = 0;
	}

	public static void main (String args[]) 
	{
		//Max of 10 rows, 10 cols, but you can change it
		int [][] intArr = new int[10][10];

		int i, j, cnt, row, col;
		for (i=0; i<10; i++) {
			for (j=0; j<10; j++) {
				//initial value for each spot = -1
				//some of these spots are just place holders
				intArr[i][j] = -1;
			}
		}

		cnt = 0;
		//INPUT THE TOP ROW HERE, or make your own entry system
		String[] input = new String[3];
		input[0]="3";
		input[1]="2";
		input[2]="0";
		for (String s : input) 
		{
			intArr[0][cnt] = new Integer (s).intValue();
			cnt++;
			//count is thus the number of rows or the number of cols
		}

		tstj tstObj = new tstj();
		row = 1;
		col = 0;
		
		//Generate the patterns and print them
		gen (tstObj, intArr, cnt, row, col);
		
		//Print the total statistics
		System.out.println ("TOT=" + new Integer (tstObj.tot) +
				"  LL=" + new Integer (tstObj.tot_ll) +
				"  RL=" + new Integer (tstObj.tot_rl) +
				"  SPEC=" + new Integer (tstObj.tot_spc));
	}

	static void gen (tstj obj, int[][] srcArr, int cnt, int row, int col) 
	{
		/*This method works recursively, calling upon itself
		 * to fill the next empty spot in the GT pattern.
		 * Once all the spots are filled, it moves on to the
		 * next possible entry in the first empty spot, then the second, etc.
		 * Thus, the method will call itself for every possible
		 * entry of every empty spot.
		 */
		
		//row and col are the current "spot" we're filling in
		
		int i, j, nxt_row, nxt_col, max;
		
		//Destination array setup
		int [][] dstArr = new int[10][10];
		for (i=0; i<10; i++) 
		{
			for (j=0; j<10; j++) 
			{
				//Copy source array
				dstArr[i][j] = srcArr[i][j];
			}
		}

		//gets the maximum value of the spot, which depends on the value to the upper left
		/*the distinction made by the if+else is necessary because
		 * the array we're using is a square, not a triangle,
		 * and everything is shifted
		 */
		if (col==0)
			max = dstArr[row-1][0];
		else
			max = dstArr[row][col-1];

		//if we've reached the end of the pattern, calculate stuff
		if (row == cnt) 
		{
			if (good_grid (obj, dstArr, cnt)) 
			{
				print_grid (dstArr, cnt);
			}
			return;
		}

		//Otherwise, this gets the next empty spot
		if (col < cnt - row - 1) 
		{
			nxt_row = row;
			nxt_col = col+1;
		}
		else 
		{
			nxt_row = row + 1;
			nxt_col = 0;
		}

		//This calls the method to generate all the patterns with
		//all the possible entries in the next empty spot
		for (i=max; i>=0; i--) 
		{
			dstArr[row][col] = i;
			gen (obj, dstArr, cnt, nxt_row, nxt_col);
		}
	}

	static boolean good_grid (tstj obj, int[][] srcArr, int cnt) 
	{
		int i, j, val;
		int ll, rl, spc;

		//Test to see if the pattern is valid
		//If not, returns false and does nothing
		//THIS IS WHERE YOU CAN EDIT TO MAKE
		//THE GT PATTERN STRICT OR NON-STRICT
		for (i=1; i<cnt; i++)
		{
			for (j=0; j<cnt; j++) 
			{
				val = srcArr[i][j];
				if (val == -1)
					continue;
				if (val > srcArr[i-1][j] || val < srcArr[i-1][j+1])
					return false;
			}
		}

		//By this point, we know the pattern is valid
		//Calculate the statistics in the GT pattern
		ll = rl = spc = 0;
		for (i=1; i<cnt; i++) 
		{
			for (j=0; j<cnt; j++) 
			{
				val = srcArr[i][j];
				if (val == -1)
					continue;
				if (val == srcArr[i-1][j])
					ll++;
				if (val == srcArr[i-1][j+1])
					rl++;
				if (val != srcArr[i-1][j] && val != srcArr[i-1][j+1])
					spc++;
			}
		}

		//Print the pattern's statistics
		System.out.println ("LL=" + new Integer(ll) +
				"  RL=" + new Integer(rl) +
				"  SPEC=" + new Integer(spc));

		//Add the statistics to the totals
		obj.tot = obj.tot + 1;
		obj.tot_ll = obj.tot_ll + ll;
		obj.tot_rl = obj.tot_rl + rl;
		obj.tot_spc = obj.tot_spc + spc;

		return true;
	}

	static void print_grid (int[][] srcArr, int cnt) 
	{
		int i, j, k;
		Integer val;

		for (i=0; i<cnt; i++) 
		{
			for (k=0; k<i; k++)
				System.out.print(" ");

			for (j=0; j<cnt; j++) 
			{
				val = new Integer (srcArr[i][j]);
				if (val != -1) {
					System.out.print (val);
					System.out.print (" ");
				}
			}
			System.out.println (" ");
		}
		System.out.println (" ");
	}
}




