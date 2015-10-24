
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

