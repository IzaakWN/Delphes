
TBrowser a;

void range(TH1* hist, double xmin, double xmax)
{
    hist->GetXaxis()->SetRangeUser(xmin,xmax);
    hist->Draw();
}

double meanRange(TH1* hist, double xmin, double xmax)
{
    hist->GetXaxis()->SetRangeUser(xmin,xmax);
    return hist->GetMean(1);
}

double integrate(TH1* hist, double xmin, double xmax)
{
    hist->GetXaxis()->SetRangeUser(xmin,xmax);
    return hist->Integral();
}

void norm(TH1* hist)
{
    hist->Scale(1./hist->Integral());
    hist->Draw();
}

void branchHist(TTree* tree, const char name[], Int_t nBins, Double_t xmin, Double_t xmax)
{
    TH1F* hist = new TH1F(name,name,nBins,xmin,xmax);
    
//     tree->SetBranchStatus("*",0);
//     tree->SetBranchStatus(&name,1);
    
    Float_t var;
    tree->SetBranchAddress(name,&var);

    Int_t N = (Int_t) tree->GetEntries();
    for(Long64_t i = 0; i<N; i++)
    {
        tree->GetEntry(i);
        hist->Fill(var);
    }
    
    hist->Draw();
}

